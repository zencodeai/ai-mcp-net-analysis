#!/bin/bash

# Source the common script
source ./docker-common.sh

# Build the Docker image
cp ../pyproject.toml .
docker build -t $PROJECT_NAME .
