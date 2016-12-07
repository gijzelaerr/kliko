import json
import logging
import os
import sys
import tempfile
from shutil import copyfile

logger = logging.getLogger(__name__)


def prepare_io(parameters, io, input_path=False, output_path=False, work_path=False, param_files_path=False):
    """
    args:
        parameters: A dict containing the parameters
        io (str): split or join
        input_path:  input path, defaults to $(pwd)/input
        output_path: output path, defaults to $(pwd)/output
        work_path: work path, defaults to $(pwd)/work
        param_files_path: param_files_path path, defaults to $(pwd)/input
    returns:
        tuple: (path to parameters file,  input, output, work, param_files)
    """
    here = os.getcwd()

    if io == 'split':
        if not input_path:
            input_path = os.path.join(here, 'input')

        if not os.path.exists(input_path):
            raise IOError("input path '%s' doesn't exist" % input_path)

        if not output_path:
            output_path = os.path.join(here, 'output')

        if not os.path.exists(output_path):
            os.mkdir(output_path)

    elif io == 'join':
        if not work_path:
            work_path = os.path.join(here, 'work')

        if not os.path.exists(work_path):
            raise IOError("work path '%s' doesn't exist" % work_path)

    if sys.platform == "darwin":
        # tempfolder not mounted into docker virtual machine
        parameters_path = os.path.join(here, 'parameters.json')
        parameters_file = open(parameters_path, 'w')

        if not param_files_path:
            param_files_path = os.path.join(here, 'param_files')
        if not os.path.exists(param_files_path):
            os.mkdir(param_files_path)
    else:
        _, parameters_path = tempfile.mkstemp()
        parameters_file = open(parameters_path, 'w')
        param_files_path = tempfile.mkdtemp()

    parameters_file.write(parameters)
    parameters_file.close()
    return parameters_path, input_path, output_path, work_path, param_files_path


def kliko_runner(kliko_data, parameters, input_path, output_path, work_path, docker_client, image_name):
    io = kliko_data['io']
    parameters_string = json.dumps(parameters)
    parameters_path, input_path, output_path, work_path, param_files_path = prepare_io(parameters_string,
                                                                                       io=io,
                                                                                       input_path=input_path,
                                                                                       output_path=output_path,
                                                                                       work_path=work_path)

    logging.info("* KLIKO io: {}".format(io))
    logging.info("* KLIKO parameters_path: {}".format(parameters_path))
    logging.info("* KLIKO param_files_path: {}".format(param_files_path))
    if io == "joined":
        logging.info("* KLIKO work_path: {}".format(work_path))
    else:
        logging.info("* KLIKO input_path: {}".format(input_path))
        logging.info("* KLIKO output_path: {}".format(output_path))

    files = []
    for section in kliko_data['sections']:
        for field in section['fields']:
            if field['type'] == 'file':
                files.append((field['name'], parameters[field['name']]))

    for fieldname, path in files:
        if path:
            copyfile(path, os.path.join(param_files_path, fieldname))

    if io == 'split':
        binds = [
            input_path + ':/input:ro',
            output_path + ':/output:rw',
            parameters_path + ':/parameters.json:ro',
            param_files_path + ':/param_files:ro',
        ]

    else:
        binds = [
            work_path + ':/work:rw',
            parameters_path + ':/parameters.json:ro',
            param_files_path + ':/param_files:ro',
        ]

    host_config = docker_client.create_host_config(binds=binds)

    container = docker_client.create_container(image=image_name, host_config=host_config, command='/kliko')
    logger.info("* KLIKO container {} created from image {}".format(container['Id'], image_name))
    docker_client.start(container)
    logger.info("* KLIKO starting container {}".format(container['Id']))
    warnings = container.get('Warnings')
    if warnings:
        for warning in warnings:
            logging.warning(warning)
    for line in docker_client.logs(container, stdout=True, stderr=True, stream=True):
        try:
            logging.info(line.decode('utf-8')[:-1])  # decode and remove endline
        except UnicodeEncodeError:
            logging.error("* KLIKO utf8 decode error: " + str(line))
    error_code = docker_client.wait(container)
    logger.info("* KLIKO container {} finished, removing...".format(container['Id']))
    docker_client.remove_container(container)  # always clean up the container
    if error_code != 0:
        logging.error("* KLIKO container error code is {}".format(error_code))
        exit(1)