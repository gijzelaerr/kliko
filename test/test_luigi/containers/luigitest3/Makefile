VERSION=0.1
DOCKER_REPO=kliko/luigitest3:$(VERSION)


.PHONY: build clean run kliko


all: kliko

force-build:
	docker build --no-cache -t ${DOCKER_REPO} .

build:
	docker build -t ${DOCKER_REPO} .


clean:
	docker rmi ${DOCKER_REPO}

run: build
	docker run -ti ${DOCKER_REPO}

kliko: build
	kliko-run ${DOCKER_REPO} --arg2 arg2
