import unittest
from kliko.validate import validate_opened

intlist_kliko = {'io': 'split',
                 'schema_version': 4,
                 'container': 'kliko/minimal',
                 'sections': [{'name': 'section1',
                               'description': 'section one',
                               'fields': [
                                    {'name': 'intlist', 'type': 'List[int]'}]}]}

intlist_param = {'intlist': [1, 2, 3, 4]}
intlist_param_invalid = {'intlist': ['1', '2', '3', '4']}


class TestListTypes(unittest.TestCase):
    def test_int_list(self):
        validate_opened(intlist_kliko, intlist_param)

    def test_invalid_int_list(self):
        with self.assertRaises(Exception):
            validate_opened(intlist_kliko, intlist_param)

    def test_bool_list(self):
        pass

    def test_file_list(self):
        pass

    def test_float_list(self):
        pass

    def test_str_list(self):
        pass
