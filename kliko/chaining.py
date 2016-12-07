from hashlib import sha256
import os
import logging
import yaml
from kliko.docker_util import extract_params
from kliko.validate import validate_kliko
from kliko.core import kliko_runner


logger = logging.getLogger(__name__)


def mkdir_if_not_exists(dir):
    if os.path.isdir(dir):
        logger.info("{} exists, not creating".format(dir))
    else:
        logger.info("creating {}...".format(dir))
        os.mkdir(dir)


def dict2sha256(dict_):
    return sha256(str(frozenset(dict_.items())).encode('utf-8')).hexdigest()


def run_chain(steps, docker_client, kliko_dir=None):
    if not kliko_dir:
        here = os.getcwd()
        kliko_dir = os.path.join(here, ".kliko")

    if not os.path.isdir(kliko_dir):
        os.mkdir(kliko_dir)

    previous_output = None

    for image_name, parameters in steps:
        img_list = docker_client.images(name=image_name)
        if len(img_list) == 0:
            raise Exception("image {} not found".format(img_list))
        if len(img_list) > 1:
            raise Exception("image {} matches {} images".format(img_list, len(img_list)))
        docker_image = img_list[0]
        id_ = docker_image['Id'][7:]
        short_id = id_[:12]

        image_folder = os.path.join(kliko_dir, short_id)
        mkdir_if_not_exists(image_folder)
        raw_kliko_data = extract_params(docker_client, image_name)
        kliko_data = validate_kliko(yaml.safe_load(raw_kliko_data))
        para_hash = dict2sha256(parameters)
        short_para_hash = para_hash[:12]
        instance_path = os.path.join(image_folder, short_para_hash)
        mkdir_if_not_exists(instance_path)
        finished_path = os.path.join(instance_path, 'FINISHED')

        if kliko_data['io'] == 'split':
            if not previous_output:
                input_path = os.path.join(instance_path, 'input')
            else:
                input_path = previous_output

            mkdir_if_not_exists(input_path)
            output_path = os.path.join(instance_path, 'output')
            mkdir_if_not_exists(output_path)
            work_path = None
            previous_output = output_path
        if kliko_data['io'] == 'join':
            if not previous_output:
                work_path = os.path.join(instance_path, 'work')
            else:
                work_path = previous_output
            mkdir_if_not_exists(work_path)
            input_path = None
            output_path = None
            previous_output = work_path

        if os.access(finished_path, os.R_OK):
            logger.info("free lunch! task {} ({}) already finished! skipping.".format(short_id, image_name))
            continue

        open(finished_path, 'a').close()

        kliko_runner(kliko_data=kliko_data,
                     parameters=parameters,
                     work_path=work_path,
                     input_path=input_path,
                     output_path=output_path,
                     docker_client=docker_client,
                     image_name=image_name)


