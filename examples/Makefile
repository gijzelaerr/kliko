DOCKER_REPO=radioastro/klikotest


.PHONY: build clean


all: build


build:
	docker build -t ${DOCKER_REPO} .

clean:
	docker rmi ${DOCKER_REPO}

save: build
	export CONTAINER=$(shell docker run -d ${DOCKER_REPO} true)
	docker export -o ${DOCKER_REPO}.tar ${CONTAINER}

run: build
	docker run -ti ${DOCKER_REPO}

