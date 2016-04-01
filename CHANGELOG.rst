0.6
===

* Added a command line kliko image runner (``kliko-run``)
* Kliko entrypoint is now /kliko. This makes it easier to integrate kliko with existing containers
* parameters file is now consistently in ``/parameters.json``.

0.3
===

* Increased schema version to number 2
* Added IO type to schema (split or join)
* renamed /param_spec.yml to /kliko.yml
* also parse the required field when generating django form
