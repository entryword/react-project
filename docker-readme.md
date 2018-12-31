# Docker environment

This readme is to help developers build local environment with docker and docker-compose.

## Build

Install docker and docker-compose on your local machine first, then do the following,
```
$ docker-compose build
```
and your local image will start to build.
Make sure you are executing commands at the root of the repo (where `docker-compose.yaml` is).

## Usage
```
$ docker-compose up -d
```
will trigger your environment to go live.
```
$ docker-compose down
```
will stop the service and clean up the stopped containers.

If you want to access specific container to debug, e.g., `app` container:
```
$ docker-compose exec app bash
```