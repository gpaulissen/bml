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

# Where can we find the BML files? 
BML_FILES = $(shell perl -MFile::Spec -e 'print File::Spec->canonpath(File::Spec->rel2abs(q(test/data)))')

ifeq '$(USERPROFILE)' ''

# Linux / Mac OS X

GID = $(shell id -g)
UID = $(shell id -u)

else

# Windows

GID = 1000
UID = 1000

endif

# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help info clean build lint build-nc run up stop release publish publish-latest publish-version tag tag-latest tag-version repo-login version

.DEFAULT_GOAL := help

help: ## This help.
	@perl -ne 'printf(qq(%-30s  %s\n), $$1, $$2) if (m/^([a-zA-Z_-]+):.*##\s*(.*)$$/)' $(MAKEFILE_LIST)

# DOCKER TASKS

DOCKER_FLAGS := --log-level "info"
DOCKER := docker $(DOCKER_FLAGS)

build: ## Build the container.
	@-$(DOCKER) rmi $(APP_NAME)
	$(DOCKER) build -t $(APP_NAME) .

lint: ## Verify the container.
	$(DOCKER) scan $(APP_NAME)

build-nc: ## Build the container without caching.
	$(DOCKER) build --no-cache -t $(APP_NAME) .

DOCKER_RUN_FLAGS := -i -t --rm

run: ## Run container on port configured in `config.env` using CMD variable as the make command line and BML_FILES as the BML files directory.
	$(DOCKER) run $(DOCKER_RUN_FLAGS) \
--env-file=./config.env \
-v$(BML_FILES):/bml/files \
-e GID=$(GID) \
-e UID=$(UID) \
-p=$(PORT):$(PORT) \
--name="$(APP_NAME)" \
$(APP_NAME) \
$(CMD)

up: build run ## Run container on port configured in `config.env` (Alias to run).

stop: ## Stop and remove a running container.
	$(DOCKER) stop $(APP_NAME); $(DOCKER) rm $(APP_NAME)

release: build-nc publish ## Make a release by building and publishing the `{version}` and `latest` tagged containers to ECR.

# Docker publish.
publish: repo-login publish-latest publish-version ## Publish the `{version}` and `latest` tagged containers to ECR

publish-latest: tag-latest ## Publish the `latest` tagged container to ECR.
	@echo 'publish latest to $(DOCKER_REPO)'
	$(DOCKER) push $(DOCKER_REPO)/$(APP_NAME):latest

publish-version: tag-version ## Publish the `{version}` tagged container to ECR.
	@echo 'publish $(VERSION) to $(DOCKER_REPO)'
	$(DOCKER) push $(DOCKER_REPO)/$(APP_NAME):$(VERSION)

# Docker tagging
tag: tag-latest tag-version ## Generate container tags for the `{version}` and `latest` tags.

tag-latest: ## Generate container `{version}` tag.
	@echo 'create tag latest'
	$(DOCKER) tag $(APP_NAME) $(DOCKER_REPO)/$(APP_NAME):latest

tag-version: ## Generate container `latest` tag.
	@echo 'create tag $(VERSION)'
	$(DOCKER) tag $(APP_NAME) $(DOCKER_REPO)/$(APP_NAME):$(VERSION)

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
