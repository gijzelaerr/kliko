=============================================================
KLIKO - Scientific Compute Container Specification and Parser
=============================================================

About
-----

KLIKO is a specification, validator and parser for the KLIKO Scientific Compute Container specification.  It enables a developer of scientific software to structure the input, output and parameters of a dockerized compute task. KLIKO is written in Python.


Installation
------------

You can install Kliko inside a docker container or just on your system::

    $ python setup.py install


or from pypi::

    $ pip install kliko


Usage
-----

::

    import kliko.validate
    kliko.validate.validate('/kliko.yml', '/parameters.json')

or::

    $ kliko-validate.py /kliko.yml


Documentation
-------------

The documentation can be found on http://kliko.readthedocs.org


Example
-------

There are examples of a kliko and parameters file in the ``examples`` folder.



Travis build status
-------------------

.. image:: https://travis-ci.org/gijzelaerr/kliko.svg?branch=master
    :target: https://travis-ci.org/gijzelaerr/kliko

.. image:: https://coveralls.io/repos/github/gijzelaerr/kliko/badge.svg?branch=master
    :target: https://coveralls.io/github/gijzelaerr/kliko?branch=master

