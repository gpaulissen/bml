# Introduction

This README describes how to build, release, publish and run Docker.

## Introduction

The following files are based on templates from [mpneuried / Makefile](https://gist.github.com/mpneuried/0594963ad38e68917ef189b4e6a269db):
- config.env
- deploy.env
- docker.mk (copied from template Makefile)

# Usage

## Help

```
make -f docker.mk help
```

## Build the container with different config and deploy file

```
make -f docker.mk cnf=<another config.env> dpl=<another deploy.env> build
```

