#!/bin/bash

# Source the common script
source ./docker-common.sh

# Run the Docker image with a bash shell
docker run --rm -i --init --network host --privileged --name ${PROJECT_NAME}-tmp ${PROJECT_NAME}

