DOCKER_REPO=kliko/fitsdoublerjoined

.PHONY: build clean

all: run


build:
	docker build -t ${DOCKER_REPO} .

clean:
	docker rmi ${DOCKER_REPO}

run: build
	kliko-run kliko/fitsdoubler

