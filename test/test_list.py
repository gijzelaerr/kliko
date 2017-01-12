import unittest
from kliko.validate import validate_opened
from copy import deepcopy

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
float_param_invalid = {'list': [1, 2, 3, 4]}

str_kliko = deepcopy(base_kliko)
str_kliko['sections'][0]['fields'] = [{'name': 'list', 'type': 'List[str]'}]
str_param = {'list': ['1', '2', '3', '4']}
str_param_invalid = {'list': [1, 2, 3, 4]}


class TestListTypes(unittest.TestCase):
    def test_int_list(self):
        validate_opened(int_kliko, int_param)

    def test_invalid_int_list(self):
        with self.assertRaises(Exception):
            validate_opened(int_param_invalid, int_param)

    def test_bool_list(self):
        x = bool_kliko
        validate_opened(bool_kliko, bool_param)

    def test_invalid_bool_list(self):
        with self.assertRaises(Exception):
            validate_opened(bool_param_invalid, bool_param)

    def test_file_list(self):
        validate_opened(file_kliko, file_param)

    def test_invalid_file_list(self):
        with self.assertRaises(Exception):
            validate_opened(file_param_invalid, file_param)

    def test_float_list(self):
        validate_opened(float_kliko, float_param)

    def test_invalid_float_list(self):
        with self.assertRaises(Exception):
            validate_opened(float_param_invalid, float_param)

    def test_str_list(self):
        validate_opened(str_kliko, str_param)

    def test_invalid_str_list(self):
        with self.assertRaises(Exception):
            validate_opened(str_param_invalid, str_param)
