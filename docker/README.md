# Introduction

This directory contains Docker files and Make files to build, release, publish and run Docker.

## Template Makefile

The following files inside this directory are based on
[mpneuried / Makefile](https://gist.github.com/mpneuried/0594963ad38e68917ef189b4e6a269db):
- config.env
- deploy.env
- docker.mk (used Makefile as template)

The version.sh file is not copied since the version can be derived from the
../__about__.py file.

The usage.sh file is partly incorporated in this README.

# Operations

## Build the container

```
make build
```

## Verify the container

```
make lint
```

<!--

## Build and release the container

```
make release
```

## Publish a container to AWS-ECR.
## This includes the login to the repo

```
make publish
```

-->

## Run the container

```
make run
```

## Build and run the container

```
make up
```

## Stop the running container

```
make stop
```

## Build the container with different config and deploy file

```
make cnf=another_config.env dpl=another_deploy.env build
```

