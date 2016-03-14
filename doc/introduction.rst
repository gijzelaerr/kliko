============
Introduction
============

KLIKO is a specification, validator and parser for the Scientific Compute Container specification. KLIKO is written in
Python.


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