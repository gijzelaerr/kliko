import pkg_resources

from kliko.cli import generate_kliko_cli_parser
from kliko.kliko_docker import extract_params

try:
    __version__ = pkg_resources.require("radiopadre")[0].version
except pkg_resources.DistributionNotFound:
    __version__ = "dev"
