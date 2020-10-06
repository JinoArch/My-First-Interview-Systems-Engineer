#!/bin/bash -xe

CONTAINER=$1

if [[ "$CONTAINER" == "" ]]; then
  # if no id given simply just connect to the first running container
  CONTAINER=$(docker ps | grep -Eo "^[0-9a-z]{8,}\b")
fi

sudo docker exec -i -t $CONTAINER bash -c "apt-get update; apt-get install apt-get install openssh-server; service ssh status; service ssh start ; passwd "$2" --stdin"

