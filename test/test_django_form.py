import os
import unittest
import yaml
from django import setup

# we need to init django before we can import django_form
os.environ['DJANGO_SETTINGS_MODULE'] = 'test.test_settings'
setup()

import kliko.django_form

here = os.path.dirname(os.path.realpath(__file__))
kliko_file = os.path.join(here, "../examples/kliko.yml")


class TestDjangoForm(unittest.TestCase):
    def setUp(self):
        pass

    def test_django_form(self):
        with open(kliko_file, 'r') as f:
            parsed = yaml.load(f)

        Form = kliko.django_form.generate_form(parsed)
        form = Form()
        form.is_valid()
