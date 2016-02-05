================================================
KLILO - Scientific Compute Container Spec Parser
================================================

About
-----

About KLIKO


Installation
------------

::

    $ python setup.py install


or::

    $ pipi install kliko



The specification
-----------------

 * All is based on standard docker containers
 * Container mush have a /run.sh script, which will be used as the entrypoint command to start the container.
 * We define two types of compute containers, split IO and joined IO containers.
 * For split IO Input files will be mounted read only into /input. Output file should be written to /output, which will
   be mounted by the host.
 * For joined IO containers input & output is the /work folder which will be mounted RW.
 * parameters can be defined with a file in json format called parameters.json in /input
 * Which parameters the container will aceept should be defined in a yaml file /para_def.yml
 * The parameters definition (para_def.yml) file should follow the schema defined in kliko/schema.yml.
 * an example parameters definition file can be found in examples/form.yml



