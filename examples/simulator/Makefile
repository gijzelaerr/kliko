DOCKER_REPO=kliko/simulator


.PHONY: build force-build clean run


all: run


build:
	docker build -t ${DOCKER_REPO} .

force-build:
	docker build --no-cache -t ${DOCKER_REPO} .

clean:
	docker rmi ${DOCKER_REPO}

run: build
	kliko-run ${DOCKER_REPO} 
