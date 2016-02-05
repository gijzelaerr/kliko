from pykwalify.core import Core
import yaml
import os


here = os.path.dirname(os.path.realpath(__file__))

schema_file = os.path.join(here, "schema.yml")
schema_str = open(schema_file, 'r').read()
schema = yaml.load(schema_str)


def validate(str_):
    # first try to parse it, to make sure it is parsable
    parsed = yaml.load(str_)

    c = Core(source_data=parsed, schema_files=[schema_file])
    c.validate(raise_exception=True)
    return yaml.load(str_)