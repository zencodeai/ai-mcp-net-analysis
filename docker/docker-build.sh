#!/bin/bash

# Source the common script
source ./docker-common.sh

# Build the Docker image
# cp ../pyproject.toml .
cd $PROJECT_ROOT && docker build -t $PROJECT_NAME -f $PROJECT_ROOT/docker/Dockerfile $PROJECT_ROOT
