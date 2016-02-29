#!/usr/bin/env bash

DOCKER_REPO=klikotest

docker rmi ${DOCKER_REPO}
docker build -t ${DOCKER_REPO} .
CONTAINER=`docker run -d ${DOCKER_REPO} true`
sleep 1
docker export -o ${DOCKER_REPO}.tar ${CONTAINER}

