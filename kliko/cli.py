"""
Command line utilities for Kliko
"""
import argparse


def generate_cli(kliko_data):
    """
    Generate a command line interface from a Kliko structure.

    Args:
        kliko_data (dict): A nested kliko structure

    Returns:
        argparse.ArgumentParser: a configured argument parser

    """
    parser = argparse.ArgumentParser(description=kliko_data['description'])

    for section in kliko_data['sections']:
        for field in section['fields']:

            args = ['--' + field['name']]

            kwargs = {'dest': field['name']}

            help = ""

            if 'label' in field:
                help += field['label']
                if 'help_text' in field:
                    help += ", "

            if 'help_text' in field:
                help += field['help_text']

            if 'initial' in field:
                kwargs['default'] = field['initial']
                help += " (default: %s)" % field['initial']

            if 'required' in field:
                kwargs['required'] = field['required']

            if help:
                kwargs['help'] = help

            parser.add_argument(*args, **kwargs)
    return parser
