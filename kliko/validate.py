from pykwalify.core import Core
import yaml
import os


here = os.path.dirname(os.path.realpath(__file__))

SCHEMA_VERSION = 2


def validate_kliko(str_, version=SCHEMA_VERSION):
    """
    validate a kliko yaml string

    args:
        str_ (str): a yaml string

    returns:
        dict: a (nested) kliko structure

    raises:
        an exception if the string can't be parsed or is not in the following the Kliko schema
    """
    # first try to parse it, to make sure it is parsable
    parsed = yaml.load(str_)

    schema_file = os.path.join(here, "schemas/%s.yml" % version)
    c = Core(source_data=parsed, schema_files=[schema_file])
    c.validate(raise_exception=True)
    return yaml.load(str_)


def convert_to_parameters_schema(kliko):
    """
    Convert a kliko schema into a validator for the parameters generated with a kliko schema.

    args:
        kliko (str): a
    return: Data for a pykwalify validator
    """

    type_map = {
        'choice': 'str',
        'char': 'str',
        'file': 'str',
    }

    mapping = {}

    for section in kliko['sections']:
        for field in section['fields']:
            type_ = type_map.get(field['type'], field['type'])
            # TODO: we can't define multiple types:
            # https://github.com/Grokzen/pykwalify/issues/39
            mapping[field['name']] = {'type':'any'}

    return {'type': 'map', 'mapping': mapping}


def validate_parameters(parameters, kliko):
    """
    validate a paramters string

    args:
        parameters (dict): A structure that should follow the given kliko structure
        kliko (dict): A nested dict which defines the valid parameters in Kliko format

    returns:
        str: the parsed parameters

    raises:
        an exception if the string can't be parsed or is not in the defining valid parameters
    """
    # first try to parse it, to make sure it is parsable
    schema = convert_to_parameters_schema(kliko)
    c = Core(source_data=parameters, schema_data=schema)
    c.validate(raise_exception=True)
    return True
