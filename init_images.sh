#!/bin/bash

# Exit in case of error
set -e

export WEB_IMAGE=$DOCKERHUB_NAMESPACE/optideploy_web:latest
export DB_IMAGE=$DOCKERHUB_NAMESPACE/optideploy_db:latest


echo "Building images..."

docker build -t $WEB_IMAGE -f ./project/Dockerfile ./project
docker build -t $DB_IMAGE -f ./project/db/Dockerfile ./project/db


echo "Pushing images to Dockerhub..."

docker push $WEB_IMAGE
docker push $DB_IMAGE