#!/bin/bash

DELAY=10
DELAY_LISTENER=30

docker compose -f docker-compose.yml down
docker rm -f $(docker ps -a -q)
docker volume rm $(docker volume ls -q)

docker compose -f docker-compose.yml up -d --build

echo "****** Waiting for ${DELAY} seconds for containers to go up ******"
sleep $DELAY

docker exec mongo1 /scripts/rs-init.sh

echo "STARTING CDC LISTENER..."
docker compose -f docker-compose-listener.yml up -d --build