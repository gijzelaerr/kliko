import unittest
from pykwalify.errors import SchemaError
import kliko.validate
from kliko.testutil import kliko_data, parameters_data, kliko_file, parameters_file


class TestExample(unittest.TestCase):

    def test_validate_kliko(self):
        kliko.validate.validate_kliko(kliko_data)

    def test_convert_to_parameters_schema(self):
        kliko.validate.convert_to_parameters_schema(kliko_data)

    def test_validate_parameters(self):
        kliko.validate.validate_parameters(parameters_data, kliko_data)

    def test_validate(self):
        kliko.validate.validate(kliko_file, parameters_file)

    def test_validate_kliko_file_missing(self):
        with self.assertRaises(IOError):
            kliko.validate.validate('/non_existing_kliko_file', parameters_file)

    def test_validate_parameters_file_missing(self):
        with self.assertRaises(IOError):
            kliko.validate.validate(kliko_file, '/non_existing_parameters_file')

    def test_missing_field(self):

        kliko_data = {'sections': [{'name': 'section',
                                    'fields': [{'name': 'required',
                                                'type': 'float',
                                                'required': True}]
                                    }]
                      }
        parameters_data = {}
        with self.assertRaises(SchemaError):
            kliko.validate.validate_parameters(parameters_data, kliko_data)

    def test_illegal_field(self):
        kliko_data = {'sections': [{'name': 'section',
                                    'fields': [{'name': 'field',
                                                'type': 'float'}]
                                    }]
                      }
        parameters_data = {'illegal_field': 'bla'}
        with self.assertRaises(SchemaError):
            kliko.validate.validate_parameters(parameters_data, kliko_data)
