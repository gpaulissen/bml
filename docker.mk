# import config.
# You can change the default config with `make cnf="config_special.env" build`
cnf ?= config.env
include $(cnf)
CONFIG_VARS = $(shell perl -ne 'print $$1, qq(\n) if m/^\s*(\w+)\s*=/' $(cnf))
export $(CONFIG_VARS)

# import deploy config
# You can change the default deploy config with `make cnf="deploy_special.env" release`
dpl ?= deploy.env
include $(dpl)
DEPLOY_VARS = $(shell perl -ne 'print $$1, qq(\n) if m/^\s*(\w+)\s*=/' $(dpl))
export $(DEPLOY_VARS)

# grep the version from the __about__.py file
PYTHON = python
VERSION = $(shell $(PYTHON) __about__.py)

# docker CMD arguments
CMD = all
FILES = $(shell perl -MFile::Spec -e 'print File::Spec->canonpath(File::Spec->rel2abs(q(test/expected)))')

# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help init clean build lint build-nc run up stop release publish publish-latest publish-version tag tag-latest tag-version repo-login version

.DEFAULT_GOAL := help

help: ## This help.
	@perl -ne 'printf(qq(%-30s  %s\n), $$1, $$2) if (m/^([a-zA-Z_-]+):.*##\s*(.*)$$/)' $(MAKEFILE_LIST)

# DOCKER TASKS

build: ## Build the container.
	docker build -t $(APP_NAME) .

lint: ## Verify the container.
	docker scan $(APP_NAME)

build-nc: ## Build the container without caching.
	docker build --no-cache -t $(APP_NAME) .

run: ## Run container on port configured in `config.env`.
	docker run -i -t --rm --env-file=./config.env -v$(FILES):/bml/files -p=$(PORT):$(PORT) --name="$(APP_NAME)" $(APP_NAME) $(CMD)

up: build run ## Run container on port configured in `config.env` (Alias to run).

stop: ## Stop and remove a running container.
	docker stop $(APP_NAME); docker rm $(APP_NAME)

release: build-nc publish ## Make a release by building and publishing the `{version}` and `latest` tagged containers to ECR.

# Docker publish.
publish: repo-login publish-latest publish-version ## Publish the `{version}` and `latest` tagged containers to ECR

publish-latest: tag-latest ## Publish the `latest` tagged container to ECR.
	@echo 'publish latest to $(DOCKER_REPO)'
	docker push $(DOCKER_REPO)/$(APP_NAME):latest

publish-version: tag-version ## Publish the `{version}` tagged container to ECR.
	@echo 'publish $(VERSION) to $(DOCKER_REPO)'
	docker push $(DOCKER_REPO)/$(APP_NAME):$(VERSION)

# Docker tagging
tag: tag-latest tag-version ## Generate container tags for the `{version}` and `latest` tags.

tag-latest: ## Generate container `{version}` tag.
	@echo 'create tag latest'
	docker tag $(APP_NAME) $(DOCKER_REPO)/$(APP_NAME):latest

tag-version: ## Generate container `latest` tag.
	@echo 'create tag $(VERSION)'
	docker tag $(APP_NAME) $(DOCKER_REPO)/$(APP_NAME):$(VERSION)

# HELPERS

# generate script to login to aws docker repo
CMD_REPOLOGIN := "eval $$\( aws ecr"
ifdef AWS_CLI_PROFILE
CMD_REPOLOGIN += " --profile $(AWS_CLI_PROFILE)"
endif
ifdef AWS_CLI_REGION
CMD_REPOLOGIN += " --region $(AWS_CLI_REGION)"
endif
CMD_REPOLOGIN += " get-login --no-include-email \)"

# login to AWS-ECR
repo-login: ## Auto login to AWS-ECR unsing aws-cli.
	@eval $(CMD_REPOLOGIN)

version: ## Output the current version.
	@echo $(VERSION)