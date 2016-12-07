from hashlib import sha256
import os
import copy
import logging
import docker
import yaml
from kliko.docker_util import extract_params
from kliko.validate import validate_kliko
from kliko.core import kliko_runner

here = os.getcwd()

kliko_dir = os.path.join(here, ".kliko")


logger = logging.getLogger(__name__)


def mkdir_if_not_exists(dir):
    if os.path.isdir(dir):
        logger.info("{} exists, not creating".format(dir))
    else:
        logger.info("creating {}...".format(dir))
        os.mkdir(dir)


def make_hash(o):
    """
    Makes a hash from a dictionary, list, tuple or set to any level, that contains
    only other hashable types (including any lists, tuples, sets, and
    dictionaries).
    """

    if isinstance(o, (set, tuple, list)):
        return tuple([make_hash(e) for e in o])
    elif not isinstance(o, dict):
        return hash(o)

    new_o = copy.deepcopy(o)

    for k, v in new_o.items():
        new_o[k] = make_hash(v)

    return sha256(str(frozenset(new_o.items())).encode('utf-8')).hexdigest()



def run_chain(images):
    if not os.path.isdir(kliko_dir):
        os.mkdir(kliko_dir)

    docker_client = docker.Client()

    for image_name in images:
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
        parameters = {}   # set the parameters here

        kliko_data.update(parameters)
        para_hash = make_hash(kliko_data)
        short_para_hash = para_hash[:12]

        instance_path = os.path.join(image_folder, short_para_hash)

        mkdir_if_not_exists(instance_path)

        input_path = os.path.join(instance_path, 'input')
        mkdir_if_not_exists(input_path)
        output_path = os.path.join(instance_path, 'output')
        mkdir_if_not_exists(output_path)
        work_path = os.path.join(instance_path, 'work')
        mkdir_if_not_exists(work_path)
        kliko_runner(kliko_data, parameters, input_path, output_path, work_path, docker_client, image_name)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run_chain(['kliko/simms', 'kliko/meqtree-pipeliner', 'kliko/wsclean'])