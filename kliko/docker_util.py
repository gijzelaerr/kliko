"""
Helper functions for using Kliko in combinaton with Docker
"""
from __future__ import absolute_import
import logging
import docker.errors
from kliko.exceptions import KlikoException
import requests.exceptions

logger = logging.getLogger(__name__)


def extract_params(docker_client, image_name):
    """
    args:
        docker_client (docker.docker.Client): a docker client object
        image_name (str): name of the image to use for kliko.yml extraction
    returns:
        str: content of the param schema
    """
    try:
        container = docker_client.create_container(image=image_name,
                                                   command=['/bin/cat', '/kliko.yml'])
        docker_client.start(container)
        error_code = docker_client.wait(container)
        warnings = container.get('Warnings')
        if warnings:
            for warning in warnings:
                logger.warning(warning)
        stdout = docker_client.logs(container, stdout=True, stream=False).decode('utf-8')
        docker_client.remove_container(container)  # always clean up the container
        if error_code != 0:
            raise KlikoException(stdout.strip())
        return stdout
    except requests.exceptions.ConnectionError:
        msg = "can't connect to docker daemon"
        logging.error(msg)
        raise IOError(msg)
    except docker.errors.NotFound:
        msg = "Can't find docker image '{}'".format(image_name)
        logging.error(msg)
        raise IOError(msg)
