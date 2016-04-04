"""
Command line utilities for Kliko
"""
import argparse
import json
import os
import sys
import tempfile
from shutil import copyfile

import docker
import docker.utils
import requests.exceptions
import yaml

from kliko.kliko_docker import extract_params
from kliko.validate import validate_kliko


def directory_exists(path):
    """check if a directory exists
    """
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError("directory doesn't exists: '%s'" % path)
    return path


def file_exists(path):
    """check if a file exists
    """
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError("file doesn't exists: '%s'" % path)
    return path


def generate_kliko_cli_parser(kliko_data, parent_parser=None):
    """
    Generate a command line parser from a Kliko structure.

    Args:
        kliko_data (dict): A nested kliko structure

    Returns:
        argparse.ArgumentParser: a configured argument parser

    """
    if parent_parser:
        parser = argparse.ArgumentParser(parents=[parent_parser])
    else:
        parser = argparse.ArgumentParser(description=kliko_data['description'])

    for section in kliko_data['sections']:
        for field in section['fields']:

            args = ['--' + field['name']]

            kwargs = {'dest': field['name']}

            type_ = field['type']
            if type_ in ('float', 'bool', 'int'):
                kwargs['type'] = eval(field['type'])
            elif type_ == 'char':
                kwargs['type'] = str
            elif type_ == 'file':
                kwargs['type'] = file_exists
            elif type_ == 'choice':
                kwargs['type'] = str
                kwargs['choices'] = field['choices']

            help = ""

            if 'label' in field:
                help += field['label']
                if 'help_text' in field:
                    help += ", "

            if 'help_text' in field:
                help += field['help_text']

            if 'initial' in field:
                kwargs['default'] = field['initial']
                help += " (default: %s)" % field['initial']

            if 'required' in field:
                kwargs['required'] = field['required']

            if help:
                kwargs['help'] = help

            parser.add_argument(*args, **kwargs)
    return parser


def prepare_io(parameters, target=None):
    """
    args:
        parameters: A dict containing the parameters
        target: output or work dir for kliko
    returns:
        tuple: (path to parameters file, path to target folder, path to input folder)
    """
    here = os.getcwd()

    if not target:
        target = os.path.join(here, 'output')

    if not os.path.exists(target):
        os.mkdir(target)

    if sys.platform == "darwin":
        # tempfolder not mounted into docker virtual machine
        parameters_file = open(os.path.join(here, 'parameters.json'), 'w')
        input_ = os.path.join(here, 'input')
        if not os.path.exists(input_):
            os.mkdir(input_)
    else:
        _, parameters_path = tempfile.mkstemp()
        parameters_file = open(parameters_path, 'w')
        input_ = tempfile.mkdtemp()

    parameters_file.write(parameters)
    parameters_file.close()
    return parameters_path, target, input_


def first_parser(argv):
    """
    This is only used when script in invoked with 0 or 1 args (should be kliko image name).
    """
    epilogue = """
This is the command line based Kliko Image runner. It enables you to run a container directly from the console.

Use:

  $ kliko-run <kliko-image> --help

to see the list of accepted arguments for the kliko image. But default kliko-run will create an output folder
in the current working folder where the results of the Kliko run are written to.

Note that you still need to download (docker pull) or build the Kliko image yourself.
"""

    parser = argparse.ArgumentParser(description='Kliko image runner', epilog=epilogue)
    parser.add_argument('image_name', type=str, help='Kliko image you want to run')
    help = 'Kliko parameters. Run --help after image_name to retreive list from image'
    parser.add_argument('IMAGE OPTIONS', type=str, nargs='*', help=help)

    parsed = parser.parse_args(argv[1:2])
    return parsed.image_name


def second_parser(argv, kliko_data):
    """
    Used when kliko image is known, so we can extract the parameters.
    """
    # we recreate parser since otherwise we have a double help conflict
    no_help_parser = argparse.ArgumentParser(description='kliko runner', add_help=False)
    no_help_parser.add_argument('image_name', type=str)
    no_help_parser.add_argument('--target_folder', type=str)

    final_parser = generate_kliko_cli_parser(kliko_data, no_help_parser)
    final_parsed = final_parser.parse_args(argv[1:])
    target = final_parsed.target_folder
    parameters = vars(final_parsed)
    parameters.pop('image_name')
    parameters.pop('target_folder')
    return parameters, target


def kliko_runner(argv):
    image_name = first_parser(argv)

    config = docker.utils.kwargs_from_env()
    if 'tls' in config:
        config['tls'].verify = False   # TODO: disalbe this for now
    docker_client = docker.Client(**config)

    try:
        raw_kliko_data = extract_params(docker_client, image_name)
    except requests.exceptions.ConnectionError:
        print("Can't connect to docker daemon (config '%s')" % str(config))
        exit(1)
    except docker.errors.NotFound:
        print("Can't find docker image '%s'" % image_name)
        exit(1)

    kliko_data = validate_kliko(yaml.safe_load(raw_kliko_data))

    parameters, target = second_parser(argv, kliko_data)
    parameters_string = json.dumps(parameters)
    parameters_file, target, input_ = prepare_io(parameters_string, target=target)

    files = []
    for section in kliko_data['sections']:
        for field in section['fields']:
            if field['type'] == 'file':
                files.append((field['name'], parameters[field['name']]))

    if kliko_data['io'] == 'split':
        binds = [
            input_ + ':/input:ro',
            target + ':/output:rw',
            parameters_file + ':/parameters.json:ro',
        ]
        for fieldname, path in files:
            copyfile(path, os.path.join(input_, fieldname))
    else:
        binds = [
            target + ':/work:rw',
            parameters_file + ':/parameters.json:ro',
        ]
        for fieldname, path in files:
            copyfile(path, os.path.join(target, fieldname))

    host_config = docker_client.create_host_config(binds=binds)

    container = docker_client.create_container(image=image_name, host_config=host_config)
    docker_client.start(container)
    error_code = docker_client.wait(container)
    warnings = container.get('Warnings')
    if warnings:
        for warning in warnings:
            print(warning)
    stdout = docker_client.logs(container, stdout=True, stream=False).decode('utf-8')
    docker_client.remove_container(container)  # always clean up the container
    print(stdout)
    if error_code != 0:
        exit(1)
