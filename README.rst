================================================
KLIKO - Scientific Compute Container Spec Parser
================================================

About
-----

KLIKO is a sSpecification, validator and parser for the Scientific Compute Container specification. KLIKO is written in
Python.


Installation
------------

::

    $ python setup.py install


or::

    $ pip install kliko


Usage
-----


::

    import kliko

    schema_string = open('examples/kliko.yml', 'r').read()
    parameters = open('examples/parameters.json', 'r').read()
    schema = kliko.validate_kliko(schema_string)

    kliko.validate_parameters(parameters, schema)



The specification
-----------------

 * All is based on standard docker containers
 * Container mush have a CMD specified, which would be the main program of the container. It should not require
   arguments.
 * logging should be written to STDOUT and STDERR.
 * We define two types of compute containers, split IO and joined IO containers.
 * For split IO Input files will be mounted read only into ``/input``. Output file should be written to ``/output``,
   which will be mounted by the host.
 * For joined IO containers input & output is the /work folder which will be mounted RW.
 * parameters for the computation will be given when the container is raun in the form of a file in json format called
   ``parameters.json`` in ``/input``
 * Which parameters the container will accept should be defined in a yaml file ``/kliko.yml``
 * The ``kliko.yml`` file should follow the schema defined in ``kliko/schema.yml``.
 * an example parameters definition file can be found in ``examples/form.yml``
 * fields with type file will enable supply of custom input files. these will be put in the ``/input`` folder.


Example
-------

There is an example in ``examples/form.yml``


Django
------

In ``kliko.django_form`` there is a function that can automatically generate a Django form from a parsed
parameter definition file. This is used by RODRIGUES to render a form inside a website which then can be used
to schedule a parameterized container.


https://github.com/ska-sa/rodrigues/


This requires django-form-utils.

https://pypi.python.org/pypi/django-form-utils


Travis build status
-------------------

.. image:: https://travis-ci.org/gijzelaerr/kliko.svg?branch=master
    :target: https://travis-ci.org/gijzelaerr/kliko

