#!/bin/bash

echo "Setting parameter for deployment..."

export NUMBER_DIGITALOCEAN_NODES=2
DIGITALOCEAN_IMAGE=ubuntu-20-04-x64
DIGITALOCEAN_REGION=fra1
DIGITALOCEAN_SIZE=s-1vcpu-1gb


echo "Spinning up droplets..."

for i in $(seq 1 $NUMBER_DIGITALOCEAN_NODES); do
    docker-machine create \
    --driver digitalocean \
    --digitalocean-image $DIGITALOCEAN_IMAGE \
    --digitalocean-region $DIGITALOCEAN_REGION \
    --digitalocean-size $DIGITALOCEAN_SIZE \
    --digitalocean-access-token $DIGITAL_OCEAN_ACCESS_TOKEN \
    --engine-install-url "https://releases.rancher.com/install-docker/19.03.9.sh" \
    node-$i;
done


echo "Initializing Swarm mode..."

docker-machine ssh node-1 -- docker swarm init --advertise-addr $(docker-machine ip node-1)


echo "Adding the nodes to the Swarm..."

TOKEN=`docker-machine ssh node-1 docker swarm join-token worker | grep token | awk '{ print $5 }'`

for i in $(seq 2 $NUMBER_DIGITALOCEAN_NODES); do
  docker-machine ssh node-$i \
    -- docker swarm join --token ${TOKEN} $(docker-machine ip node-1):2377;
done



echo "Deploying optideploy..."

eval $(docker-machine env node-1)
docker stack deploy --compose-file=docker-compose-swarm.yml optideploy



echo "Get the IP address..."
echo "$(docker-machine ip node-1)"