"""
Command line utilities for Kliko
"""
from __future__ import absolute_import

import argparse
import logging
import os
import yaml

import docker
from kliko.core import kliko_runner
from kliko.docker_util import extract_params
from kliko.validate import validate_kliko

logger = logging.getLogger(__name__)


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

    if kliko_data['io'] == 'split':
        parser.add_argument('--output', type=str)
        parser.add_argument('--input', type=str)
    elif kliko_data['io'] == 'join':
        parser.add_argument('--work', type=str)

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
            else:
                # we don't want to require a field with an initial value
                if 'required' in field:
                    kwargs['required'] = field['required']

            if help:
                kwargs['help'] = help

            parser.add_argument(*args, **kwargs)
    return parser


def first_parser(argv):
    """
    This is only used when script in invoked with 0 or 1 args (should be kliko image name).
    """
    epilogue = """
This is the command line based Kliko Image runner. It enables you to run a container directly from the console.

Use:

  $ kliko-run <kliko-image> --help

to see the list of accepted arguments for the kliko image. By default kliko-run will create an output folder
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

    final_parser = generate_kliko_cli_parser(kliko_data, no_help_parser)
    final_parsed = final_parser.parse_args(argv[1:])
    parameters = vars(final_parsed)

    work = False
    if 'work' in final_parsed:
        work = final_parsed.work
        parameters.pop('work')

    input_ = False
    if 'input' in final_parsed:
        input_ = final_parsed.input
        parameters.pop('input')

    output = False
    if 'output' in final_parsed:
        output = final_parsed.output
        parameters.pop('output')

    parameters.pop('image_name')
    return parameters, input_, output, work


def command_line_run(argv):
    format = '%(asctime)-15s %(message)s'
    logging.basicConfig(level=logging.INFO, format=format)
    image_name = first_parser(argv)
    logger.info("starting image {}".format(image_name))
    config = docker.utils.kwargs_from_env()
    docker_client = docker.Client(**config)
    raw_kliko_data = extract_params(docker_client, image_name)
    kliko_data = validate_kliko(yaml.safe_load(raw_kliko_data))
    parameters, input_path, output_path, work_path = second_parser(argv, kliko_data)
    paths = {
        'input': input_path,
        'output': output_path,
        'work': work_path,
    }
    kliko_runner(kliko_data=kliko_data, parameters=parameters,
                 docker_client=docker_client,
                 image_name=image_name, paths=paths)
