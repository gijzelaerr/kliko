import unittest
import tempfile
import os
import sys
import kliko.cli
from kliko.testutil import kliko_data, parameters_str

this_file = os.path.realpath(__file__)


class TestCli(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if sys.platform == "darwin":
            here = os.getcwd()
            # tempfolder not mounted into docker virtual machine
            cls.input_ = os.path.join(here, 'input')
            if not os.path.exists(cls.input_):
                os.mkdir(cls.input_)
        else:
            cls.input_ = tempfile.mkdtemp()

    def test_cli(self):
        parser = kliko.cli.generate_kliko_cli_parser(kliko_data)


    def test_prepare_io(self):

        kliko.cli.prepare_io(parameters_str, io='split', input_path=self.input_)

    def test_first_parser(self):
        with self.assertRaises(SystemExit):
            kliko.cli.first_parser(['kliko-run'])
        with self.assertRaises(SystemExit):
            kliko.cli.first_parser(['kliko-run', '--help'])
        kliko.cli.first_parser(['kliko-run', 'kliko/minimal'])

        kliko.cli.first_parser(['kliko-run', 'kliko/minimal', '--help'])

    def test_second_parser(self):
        with self.assertRaises(SystemExit):
            kliko.cli.second_parser(['kliko-run'], kliko_data)
        with self.assertRaises(SystemExit):
            kliko.cli.second_parser(['kliko-run', '--help'], kliko_data)
        with self.assertRaises(SystemExit):
            kliko.cli.second_parser(['kliko-run', 'kliko/minimal'], kliko_data)
        with self.assertRaises(SystemExit):
            kliko.cli.second_parser(['kliko-run', 'kliko/minimal', '--help'], kliko_data)

        kliko.cli.second_parser(['kliko-run', 'kliko/minimal', '--choice', 'second', '--string', 'gijs',
                                 '--file', this_file, '--int', '10'], kliko_data)

    def test_kliko_runner(self):
        with self.assertRaises(SystemExit):
            kliko.cli.kliko_runner(['kliko-run'])
        with self.assertRaises(SystemExit):
            kliko.cli.kliko_runner(['kliko-run', '--help'])
        with self.assertRaises(SystemExit):
            kliko.cli.kliko_runner(['kliko-run', 'kliko/minimal'])
        with self.assertRaises(SystemExit):
            kliko.cli.kliko_runner(['kliko-run', 'kliko/minimal', '--help'])

        kliko.cli.kliko_runner(['kliko-run', 'kliko/minimal', '--choice', 'second', '--string', 'gijs',
                                 '--file', this_file, '--int', '10', '--input', self.input_])