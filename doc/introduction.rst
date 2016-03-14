============
Introduction
============

KLIKO is a specification, validator and parser for the Scientific Compute Container specification. KLIKO is written in
Python.

installation
============

From the source folder::

    $ python setup.py install


or from pypi::

    $ pip install kliko


Getting started
===============

To get started you should:

 * Create a Docker container from your application
 * Add or modify a script in the container that can parse and use a ``parameters.json`` file.
 * Add a ``kliko.yml`` file to the root of the container which defines the valid fields in the parameters file.
 * You can validate your kliko file with the ``kliko-validate.py`` script installed by the kliko Python library.


Contributing
============

Contributions are more than welcome! If you experience any problems let us know in the bug tracker. We accept patches
in the form of github pull requests. Please make sure your code works with python 2 and python3, and is pep8 compatible.
Also make sure the test suit actually passes all tests. We use docker in some of the tests so you need to have that
installed and configured.