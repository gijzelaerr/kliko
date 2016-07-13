from os import path
import yaml
import json

here = path.dirname(path.realpath(__file__))
kliko_file = path.join(here, "../examples/minimal/kliko.yml")
parameters_file = path.join(here, "../examples/minimal/parameters.json")

with open(kliko_file, 'r') as f:
    kliko_data = yaml.load(f)

with open(parameters_file, 'r') as f:
    parameters_data = json.load(f)

parameters_str = json.dumps(parameters_data)
