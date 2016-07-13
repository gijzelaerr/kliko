====================
Inside the container
====================

Inside the kliko container you can use the kliko library to validate the
parameters file and read the settings.


validation and parsing
======================

Validating and parsing the parameters is quite simple::

    from kliko.validate import validate
    parameters = validate()

This would open read and parse the files from the default locations. The parameters
from ``/parameters.json``, which are then validated against ``/kliko.yml``.

parameter files
===============

Files defined in the ``kliko.yml`` file and specified during runtime should be copied to the ``param_file`` folder
by the kliko runner.


Environment variables
=====================

A kliko runner can have influence on the default location by setting environment
variables. these variables are:


 * ``INPUT`` (``kliko.input``) - controlling the input folder location, default ``/input``
 * ``OUTPUT`` (``kliko.output``) - controlling the input folder location, default ``/output``
 * ``WORK`` (``kliko.work``) - controlling the input folder location, default ``/work``
 * ``PARAM_FILES`` (``kliko.param_files``) - controlling the input folder location, default ``/parame_files``
 * ``KLIKO_FILE`` (``kliko.kliko_file``) - controlling the input folder location, default ``/kliko.yml``
 * ``PARAM_FILE`` (``kliko.param_file``) - controlling the input folder location, default ``/parameters.json``

 These