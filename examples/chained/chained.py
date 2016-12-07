from kliko.chaining import run_chain
import logging
import docker


logging.basicConfig(level=logging.INFO)
docker_client = docker.Client()

run_chain(
    (
        ('kliko/simms',  {'tel': 'meerkat'}),
        ('kliko/meqtree-pipeliner', {}),
        ('kliko/wsclean', {'weight': 'uniform'}),
    ),
    docker_client
)
