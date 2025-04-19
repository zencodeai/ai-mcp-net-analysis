#!/bin/bash

# Source the common script
source ./docker-common.sh

# Run the Docker image with a bash shell
# run --rm -d -p 6274:6274 -v ai-mcp-net-analysis:/app --privileged --name $ai-mcp-net-analysis-tmp /bin/bash -c "npx -y @modelcontextprotocol/inspector uv  --directory /app run ai-mcp-net-analysis/server.py"
# docker run --rm -d -p 6274:6274 -v ${PROJECT_ROOT}:/app --privileged --name ${PROJECT_NAME}-tmp ${PROJECT_NAME} /bin/bash -c "npx -y @modelcontextprotocol/inspector \
#  uv \
#  --directory /app \
#  run \
#  ai-mcp-net-analysis/server.py"
docker run --rm -i --init -it -p 6274:6274 -v ${PROJECT_ROOT}:/app --privileged --name ${PROJECT_NAME}-tmp ${PROJECT_NAME} /bin/bash
