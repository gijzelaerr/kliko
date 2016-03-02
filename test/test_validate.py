import os
import unittest
import json

import kliko.validate

here = os.path.dirname(os.path.realpath(__file__))


class TestExample(unittest.TestCase):
    def setUp(self):
        self.kliko_example = open(os.path.join(here, "../examples/kliko.yml"), 'r').read()
        self.parameters_example = open(os.path.join(here, "../examples/parameters.json"), 'r').read()

    def test_validate_kliko(self):
        kliko.validate.validate_kliko(self.kliko_example)

    def test_validate_parameters(self):
        validator = kliko.validate.validate_kliko(self.kliko_example)
        validated = json.loads(self.parameters_example)
        kliko.validate.validate_parameters(validated, validator)




