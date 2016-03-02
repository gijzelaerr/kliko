import os
import unittest
import docker
import docker.utils
from builtins import open

import kliko.docker
from kliko.exceptions import KlikoException

TEST_IMAGE = 'klikotest'

TEST_ARCHIVE = os.path.join(os.path.dirname(__file__), 'test_image/%s.tar' % TEST_IMAGE)
PARAMS_FILE = os.path.join(os.path.dirname(__file__), 'test_image/kliko.yml')


def set_fixture(docker_client, image_name, image_archive):
        if docker_client.images(name=image_name):
            docker_client.remove_image(image=image_name, force=True)
        docker_client.import_image_from_file(filename=image_archive, repository=image_name, tag='latest')


class TestUtils(unittest.TestCase):
    def setUp(self):
        config = docker.utils.kwargs_from_env()
        config['version'] = "1.20"
        self.client = docker.Client(**config)
        set_fixture(self.client, TEST_IMAGE, TEST_ARCHIVE)

    def test_extract(self):
        image_params = kliko.docker.extract_params(self.client, TEST_IMAGE)
        true_params = open(PARAMS_FILE, mode='r', encoding='utf-8').read()
        self.assertEqual(image_params, true_params)

    def test_extract_without_params(self):
        with self.assertRaises(KlikoException):
            kliko.docker.extract_params(self.client, 'alpine:3.3')
