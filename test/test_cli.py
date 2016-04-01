import unittest
import kliko.cli
from kliko.testutil import kliko_data, parameters_str


class TestCli(unittest.TestCase):
    def test_cli(self):
        parser = kliko.cli.generate_kliko_cli_parser(kliko_data)

    def test_prepare_io(self):
        kliko.cli.prepare_io(parameters_str)

    def test_first_parser(self):
        with self.assertRaises(SystemExit):
            kliko.cli.first_parser(['kliko-run'])
        with self.assertRaises(SystemExit):
            kliko.cli.first_parser(['kliko-run', '--help'])
        kliko.cli.first_parser(['kliko-run', 'radioastro/klikotest'])

        kliko.cli.first_parser(['kliko-run', 'radioastro/klikotest', '--help'])

    def test_second_parser(self):
        with self.assertRaises(SystemExit):
            kliko.cli.second_parser(['kliko-run'], kliko_data)
        with self.assertRaises(SystemExit):
            kliko.cli.second_parser(['kliko-run', '--help'], kliko_data)
        with self.assertRaises(SystemExit):
            kliko.cli.second_parser(['kliko-run', 'radioastro/klikotest'], kliko_data)
        with self.assertRaises(SystemExit):
            kliko.cli.second_parser(['kliko-run', 'radioastro/klikotest', '--help'], kliko_data)

        kliko.cli.second_parser(['kliko-run', 'radioastro/klikotest', '--choice', 'second', '--char', 'gijs',
                                 '--file', 'test_cli.py', '--int', '10'], kliko_data)

    def test_kliko_runner(self):
        with self.assertRaises(SystemExit):
            kliko.cli.kliko_runner(['kliko-run'])
        with self.assertRaises(SystemExit):
            kliko.cli.kliko_runner(['kliko-run', '--help'])
        with self.assertRaises(SystemExit):
            kliko.cli.kliko_runner(['kliko-run', 'radioastro/klikotest'])
        with self.assertRaises(SystemExit):
            kliko.cli.kliko_runner(['kliko-run', 'radioastro/klikotest', '--help'])

        kliko.cli.kliko_runner(['kliko-run', 'radioastro/klikotest', '--choice', 'second', '--char', 'gijs',
                                 '--file', 'test_cli.py', '--int', '10'])