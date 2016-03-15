import unittest
import kliko.cli
from kliko.testutil import kliko_data


class TestCli(unittest.TestCase):
    def test_cli(self):
        parser = kliko.cli.generate_cli(kliko_data)
        parser.parse_args(args=[])
