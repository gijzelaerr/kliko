Command Line Utilities
======================


kliko-run
---------

Use this to run the container. Use ``kliko-run <image-name> --help`` to see a list of accepted kliko paramaters, which
are kliko container specific.

.. note::

    On OSX Kliko-run will create a ``parameters.json`` file and a ``param_files`` folder in the current worker directory.
    Normally these are created in a temporary directory in your system, but since Docker on OSX doesn't mount
    the temporary folder into the docker virtual machine these files are inaccessable from within the docker engine
    and containers.

kliko-validate
--------------

Use this script to check if kliko container is valid.
