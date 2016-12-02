0.7.1
=====

* Run /kliko, not the default docker CMD
* Add simms example
* dont try to copy empty file field
* remove explicit pyyaml dependency


0.7
===

* Install docker by default
* Made container, author and email fields optional in specification
* Increased specification number (3)
* Don't put parameter files in /input but in /param_files
* Renamed ``char`` field type to ``str``
* Add option to override paths using environment variables (INPUT, OUTPUT, WORK,
  PARAM_FILES, KLIKO_FILE, PARAM_FILE)
* Change behavior of kliko-run, it now accepts the --input, --output, --work


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
