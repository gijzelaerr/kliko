import os
import unittest
from django import setup
from kliko.testutil import kliko_data

# we need to init django before we can import django_form
os.environ['DJANGO_SETTINGS_MODULE'] = 'test.test_settings'
setup()

import kliko.django_form


class TestDjangoForm(unittest.TestCase):
    def test_django_form(self):
        Form = kliko.django_form.generate_form(kliko_data)
        form = Form()
        form.is_valid()
