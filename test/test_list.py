import unittest
from kliko.validate import validate_opened
from copy import deepcopy
import os
from pykwalify.errors import SchemaError
from django import setup


# we need to init django before we can import django_form
os.environ['DJANGO_SETTINGS_MODULE'] = 'test.test_settings'
setup()

from kliko.django_form import generate_form

base_kliko = {'io': 'split',
                 'schema_version': 4,
                 'container': 'kliko/minimal',
                 'sections': [{'name': 'section1',
                               'description': 'section one'}]}

int_kliko = deepcopy(base_kliko)
int_kliko['sections'][0]['fields'] = [{'name': 'list', 'type': 'List[int]'}]
int_param = {'list': [1, 2, 3, 4]}
int_param_invalid = {'list': ['1', '2', '3', '4']}

bool_kliko = deepcopy(base_kliko)
bool_kliko['sections'][0]['fields'] = [{'name': 'list', 'type': 'List[bool]'}]
bool_param = {'list': [True, True, False, False]}
bool_param_invalid = {'list': ['1', '2', '3', '4']}

file_kliko = deepcopy(base_kliko)
file_kliko['sections'][0]['fields'] = [{'name': 'list', 'type': 'List[file]'}]
file_param = {'list': ['/tmp', '/etc', 'windows.cmd', '..']}
file_param_invalid = {'list': [1, 2, 3, 4]}

float_kliko = deepcopy(base_kliko)
float_kliko['sections'][0]['fields'] = [{'name': 'list', 'type': 'List[float]'}]
float_param = {'list': [0.1, 0.2, 0.3, 0.4]}
float_param_invalid = {'list': ['g', 'e', 'w', 'r']}

str_kliko = deepcopy(base_kliko)
str_kliko['sections'][0]['fields'] = [{'name': 'list', 'type': 'List[str]'}]
str_param = {'list': ['1', '2', '3', '4']}
str_param_invalid = {'list': [1, 2, 3, 4]}


class TestListTypes(unittest.TestCase):
    def test_int_list(self):
        validate_opened(int_kliko, int_param)

    def test_invalid_int_list(self):
        with self.assertRaises(SchemaError):
            validate_opened(int_param_invalid, int_param_invalid)

    def test_bool_list(self):
        validate_opened(bool_kliko, bool_param)

    def test_invalid_bool_list(self):
        with self.assertRaises(SchemaError):
            validate_opened(bool_kliko, bool_param_invalid)

    def test_file_list(self):
        validate_opened(file_kliko, file_param)

    def test_invalid_file_list(self):
        with self.assertRaises(SchemaError):
            validate_opened(file_kliko, file_param_invalid)

    def test_float_list(self):
        validate_opened(float_kliko, float_param)

    def test_invalid_float_list(self):
        with self.assertRaises(SchemaError):
            validate_opened(float_kliko, float_param_invalid)

    def test_str_list(self):
        validate_opened(str_kliko, str_param)

    def test_invalid_str_list(self):
        with self.assertRaises(SchemaError):
            validate_opened(str_kliko, str_param_invalid)


class TestDjangoList(unittest.TestCase):
    def test_django_int_list(self):
        generate_form(int_kliko)

    def test_django_bool_list(self):
        generate_form(bool_kliko)

    def test_django_file_list(self):
        generate_form(file_kliko)

    def test_django_float_list(self):
        generate_form(float_kliko)

    def test_django_str_list(self):
        generate_form(str_kliko)
