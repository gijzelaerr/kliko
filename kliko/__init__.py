import pkg_resources
import os

try:
    __version__ = pkg_resources.require("kliko")[0].version
except pkg_resources.DistributionNotFound:
    __version__ = "dev"


input_path = os.environ.get('INPUT', '/input')
output_path = os.environ.get('OUTPUT', '/output')
work_path = os.environ.get('WORK', '/work')
param_files = os.environ.get('PARAM_FILES', '/param_files')
kliko_file = os.environ.get('KLIKO_FILE', '/kliko.yml')
parameters_file = os.environ.get('PARAM_FILE', '/parameters.json')
