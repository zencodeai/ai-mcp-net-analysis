#!/bin/bash

# Source the common script
source ./docker-common.sh

# Run the Docker image with a bash shell
docker run --rm -i -it --init --network host --privileged --entrypoint /bin/bash --name ${PROJECT_NAME}-tmp ${PROJECT_NAME}

