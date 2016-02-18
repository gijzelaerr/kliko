import os
import unittest

import kliko.validate

here = os.path.dirname(os.path.realpath(__file__))


class TestExample(unittest.TestCase):
    def test_parse(self):
        example = open(os.path.join(here, "../examples/form.yml"), 'r').read()
        kliko.validate.validate(example)



