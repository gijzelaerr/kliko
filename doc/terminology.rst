Terminology
===========


Kliko
-----

A specification which defines constrains on a docker container to aid in the scheduling of scientific compute tasks.

It is also a Python library that can be used to check if a container confirms the specification.


Kliko image
-----------

A Docker image confirming to the kliko specification. An image is an ordered collection of root filesystem changes and
the corresponding execution parameters for use within a container runtime. Images are read-only.


Kliko container
---------------

A container is an active (or inactive if exited) stateful instantiation of an image.

Read more about Docker terminology in the `Docker glossary <http://docs.docker.com/reference/glossary/#container>`_.


The kliko.yml file
------------------

A yaml formatted file confirming to the Kliko specification that defines the parameters a Kliko container is expecting.
This is the file you want to create and add to your dockdr image if you want to create a Kliko container.


The parameters.json file
------------------------

A json encoded structure that contains all the parameter values for your compute task. This file is presented to your
 container at runtime by the container runner, for example RODRIGUES or Nextflow. The valid fields are defined
 by the Kliko image container and are defined in the ``kliko.yml`` file.




