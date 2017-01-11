import json
import logging
import os
from shutil import copyfile

logger = logging.getLogger(__name__)


def write_parameters_file(path, parameters):
    parameters_string = json.dumps(parameters)
    parameters_file = open(path, 'w')
    parameters_file.write(parameters_string)
    parameters_file.close()


def prepare_io(io, parameters={}, paths={}):
    """
    args:
        parameters: A dict containing the parameters
        io (str): split or join
        paths: dict of paths
    returns:
        tuple: (path to parameters file,  input, output, work, param_files)
    """

    if 'parent' in paths:
        parent = paths['parent']
    else:
        parent = os.getcwd()

    if not parameters:
        parameters = {}

    if io == 'split':
        work_path = False
        if 'input' not in paths or not paths['input']:
            input_path = os.path.join(parent, 'input')
        else:
            input_path = paths['input']

        if not os.path.exists(input_path):
            logging.warning("input folder {} doesn't exist, creating...".format(input_path))
            os.mkdir(input_path)

        if 'output' not in paths or not paths['output']:
            output_path = os.path.join(parent, 'output')
        else:
            output_path = paths['output']

        if not os.path.exists(output_path):
            os.mkdir(output_path)

    elif io == 'join':
        input_path = False
        output_path = False
        if 'work' not in paths or not paths['work']:
            work_path = os.path.join(parent, 'work')
        else:
            work_path = paths['work']

        if not os.path.exists(work_path):
            logging.warning("work folder {} doesn't exist, creating...".format(work_path))
            os.mkdir(work_path)

    if 'parameters' not in paths or not paths['parameters']:
        parameters_path = os.path.join(parent, 'parameters.json')
    else:
        parameters_path = paths['parameters']

    if 'param_files' not in paths or not paths['param_files']:
        param_files_path = os.path.join(parent, 'param_files')
    else:
        param_files_path = paths['parameters']

    if not os.path.exists(param_files_path):
        os.mkdir(param_files_path)

    return parameters_path, input_path, output_path, work_path, parameters_path, param_files_path


def kliko_runner(image_name, kliko_data, docker_client, parameters={}, paths={}):
    """

    args:
        image_name: docker image to run
        kliko_data: parsed kliko data
        docker_client: a docker client connection
        parameters: dict with kliko parameters
        paths: dict with paths. Can contain input, output, work, parameters, param_files, parent
    """

    io = kliko_data['io']
    final_paths = prepare_io(parameters=parameters, io=io, paths=paths)
    parameters_path, input_path, output_path, work_path, param_files_path, param_files_path = final_paths

    logging.info("io: {}".format(io))
    logging.info("parameters_path: {}".format(parameters_path))
    logging.info("param_files_path: {}".format(param_files_path))
    if io == "join":
        logging.info("work_path: {}".format(work_path))
    else:
        logging.info("input_path: {}".format(input_path))
        logging.info("output_path: {}".format(output_path))

    for section in kliko_data['sections']:
        for field in section['fields']:
            if field['type'] == 'file':
                fieldname = field['name']
                path = parameters[field['name']]
                copyfile(path, os.path.join(param_files_path, fieldname))
                parameters[fieldname] = '/param_files/' + fieldname

    write_parameters_file(parameters_path, parameters)

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
    logger.info("container {} created from image {}".format(container['Id'], image_name))
    docker_client.start(container)
    logger.info("starting container {}".format(container['Id']))
    warnings = container.get('Warnings')
    if warnings:
        for warning in warnings:
            logging.warning(warning)
    for line in docker_client.logs(container, stdout=True, stderr=True, stream=True):
        try:
            logging.info(line.decode('utf-8')[:-1])  # decode and remove endline
        except UnicodeEncodeError:
            logging.error("utf8 decode error: " + str(line))
    error_code = docker_client.wait(container)
    logger.info("container {} finished, removing...".format(container['Id']))

    # TODO: disabled removal for now, what do we want?
    # docker_client.remove_container(container)  # always clean up the container

    if error_code != 0:
        raise Exception("kliko container returned error code {}".format(error_code))
    else:
        logging.info("kliko container returned error code {}".format(error_code))

