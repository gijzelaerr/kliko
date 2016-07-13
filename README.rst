=============================================================
KLIKO - Scientific Compute Container Specification and Parser
=============================================================

About
-----

KLIKO is a specification, validator and parser for the KLIKO Scientific Compute Container
specification. It enables a developer of scientific software to structure the input,
output and parameters of a dockerized compute task. KLIKO is written in Python.


Installation
------------

You can install Kliko inside a docker container or just on your system::

    $ python setup.py install


or from pypi::

    $ pip install kliko


Usage
-----

from a Python script inside a container::

    from kliko.validate import validate
    parameters = validate()

or to check if a kliko file has a valid syntax::

    $ kliko-validate /kliko.yml

or try to run the docker image from the examples folder directly::

    $ kliko-run kliko/minimal --help

        usage: kliko-run [-h] [--target_folder TARGET_FOLDER] --choice {second,first}
                         --char CHAR [--float FLOAT] --file FILE --int INT
                         image_name

        positional arguments:
          image_name

        optional arguments:
          -h, --help            show this help message and exit
          --target_folder TARGET_FOLDER
          --choice {second,first}
                                choice field (default: second)
          --char CHAR           char field, maximum of 10 chars (default: empty)
          --float FLOAT         float field (default: 0.0)
          --file FILE           file field, this file will be put in /input in case of
                                split io, /work in case of join io
          --int INT             int field


Documentation
-------------

The documentation can be found on http://kliko.readthedocs.org


Example
-------

There are examples of a kliko and parameters file in the ``examples`` folder.



Travis build status
-------------------

.. image:: https://img.shields.io/travis/gijzelaerr/kliko.svg
    :target: https://travis-ci.org/gijzelaerr/kliko

.. image:: https://img.shields.io/coveralls/gijzelaerr/kliko.svg
    :target: https://coveralls.io/github/gijzelaerr/kliko?branch=master

.. image:: https://img.shields.io/pypi/v/kliko.svg
     :target: https://pypi.python.org/pypi/kliko

.. image:: https://img.shields.io/pypi/pyversions/kliko.svg
     :target: https://pypi.python.org/pypi/kliko
