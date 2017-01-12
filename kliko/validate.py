"""
Kliko and parameter validation related functions.
"""
from pykwalify.core import Core
import yaml
import json
import os
import re
from kliko import parameters_file as parameters_file_default
from kliko import kliko_file as kliko_file_default

here = os.path.dirname(os.path.realpath(__file__))

SCHEMA_VERSION = 4


def validate_kliko(kliko, version=SCHEMA_VERSION):
    """
    validate a kliko yaml string

    args:
        kliko: a parsed kliko object

    returns:
        dict: a (nested) kliko structure

    raises:
        an exception if the string can't be parsed or is not in the following the Kliko schema
    """
    # first try to parse it, to make sure it is parsable

    schema_file = os.path.join(here, "schemas/%s.yml" % version)
    c = Core(source_data=kliko, schema_files=[schema_file])
    c.validate(raise_exception=True)
    return kliko


list_regex = re.compile('List\[(int|float|bool|file|str)\]')

type_map = {
    'choice': 'str',
    'char': 'str',
    'file': 'str',
}


def convert_to_parameters_schema(kliko):
    """
    Convert a kliko schema into a validator for the parameters generated with a kliko schema.

    args:
        kliko (str): a kliko definition
    returns:
        A structure for a pykwalify validator
    """
    mapping = {}

    for section in kliko['sections']:
        for field in section['fields']:
            value = {'required': 'required' in field}

            # check if field is a list
            match = list_regex.match(field['type'])
            if match:
                value['type'] = 'seq'
                matchtype = match.group(1)
                value['sequence'] = [{'type': type_map.get(matchtype, matchtype)}]
            # otherwise check if it is a choice
            elif field['type'] == 'choice':
                value['type'] = 'str'
                value['enum'] = list(field['choices'].keys())
            else:
                value['type'] = type_map.get(field['type'], field['type'])

            mapping[field['name']] = value

    return {'type': 'map', 'mapping': mapping}


def validate_parameters(parameters, kliko):
    """
    validate a set of parameters given a kliko definition

    args:
        parameters (dict): A structure that should follow the given kliko structure
        kliko (dict): A nested dict which defines the valid parameters in Kliko format

    returns:
        str: the parsed parameters

    raises:
        an exception if the string can't be parsed or is not in the defining valid parameters
    """
    schema = convert_to_parameters_schema(kliko)
    c = Core(source_data=parameters, schema_data=schema)
    c.validate(raise_exception=True)
    return True


def validate(kliko_file=False, paramaters_file=False):
    """
    Validate the kliko and paramaters file and parse the parameters file. Should be run inside
    the Kliko container.

    Args:
        kliko_file (str):  Path to a kliko file
        paramaters_file (str): path to a parameters file

    Returns:
        The validated and parsed paramaters file
    """
    kliko_file = kliko_file or kliko_file_default
    paramaters_file = paramaters_file or parameters_file_default

    with open(kliko_file, 'r') as f:
        kliko = yaml.safe_load(f)

    with open(paramaters_file, 'r') as f:
        parameters = json.load(f)

    return validate_opened(kliko, parameters)


def validate_opened(kliko, parameters):
    validate_kliko(kliko)
    validate_parameters(parameters, kliko)

    defaults = {}
    for section in kliko['sections']:
        for field in section['fields']:
            if 'initial' in field:
                defaults[field['name']] = field['initial']

    defaults.update(parameters)
    return defaults
