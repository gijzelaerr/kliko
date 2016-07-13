import os
import unittest
import docker
import docker.utils
from builtins import open

import kliko.docker
from kliko.exceptions import KlikoException

TEST_IMAGE = 'kliko/minimal'


PARAMS_FILE = os.path.join(os.path.dirname(__file__), '../examples/minimal/kliko.yml')


class TestUtils(unittest.TestCase):
    def setUp(self):
        config = docker.utils.kwargs_from_env()
        config['version'] = "1.20"
        self.client = docker.Client(**config)
        self.assertTrue(self.client.images(name=TEST_IMAGE), "docker image %s not found" % TEST_IMAGE)

    def test_extract(self):
        image_params = kliko.docker.extract_params(self.client, TEST_IMAGE)
        true_params = open(PARAMS_FILE, mode='r', encoding='utf-8').read()
        self.assertEqual(image_params, true_params)

    def test_extract_without_params(self):
        with self.assertRaises(KlikoException):
            kliko.docker.extract_params(self.client, 'python:3.5')
