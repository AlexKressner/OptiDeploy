#!/bin/bash

echo "Removing stack and droplets..."

eval $(docker-machine env node-1)
docker stack rm optideploy
for i in $(seq 1 $NUMBER_DIGITALOCEAN_NODES); do
    docker-machine rm node-$i -y
done
