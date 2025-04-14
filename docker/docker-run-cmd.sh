#!/bin/bash

# Source the common script
source ./docker-common.sh

# Run the Docker image with a bash shell
docker run --rm -it -v ${PROJECT_ROOT}:/app --network host --privileged --name ${PROJECT_NAME}-tmp ${PROJECT_NAME} /bin/bash

