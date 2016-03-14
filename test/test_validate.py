import os
import unittest
import json
import yaml

import kliko.validate

here = os.path.dirname(os.path.realpath(__file__))
kliko_file = os.path.join(here, "../examples/kliko.yml")
parameters_file = os.path.join(here, "../examples/parameters.json")


class TestExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(kliko_file, 'r') as f:
            cls.kliko_data = yaml.safe_load(f)

        with open(parameters_file, 'r') as f:
            cls.parameters_data = json.load(f)

    def test_validate_kliko(self):
        kliko.validate.validate_kliko(self.kliko_data)

    def test_convert_to_parameters_schema(self):
        kliko.validate.convert_to_parameters_schema(self.kliko_data)

    def test_validate_parameters(self):
        kliko.validate.validate_parameters(self.parameters_data, self.kliko_data)

    def test_validate(self):
        kliko.validate.validate(kliko_file, parameters_file)




