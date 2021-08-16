#!/bin/bash

echo "Removing stack and droplets..."

eval $(docker-machine env node-1)
docker stack rm optideploy
docker-machine rm $(docker-machine ls -q) -y
