#!/bin/bash -x
# Wrap docker-compose around a shell script in order to set
#  variables to use in docker-compose "networks:" config
source .env
export INTERFACE
export SUBNET
# echo $(envsubst < docker-compose.yml)
# docker-compose -f <(envsubst < docker-compose.yml) $@
docker-compose -f docker-compose.yml $@
