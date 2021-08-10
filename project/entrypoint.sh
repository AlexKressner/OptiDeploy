#!/bin/sh

echo "Waiting for mongo..."

while ! nc -z mongodb 27017; do
  sleep 0.25
done

echo "Mongodb started"



echo "Waiting for rabbitmq..."

while ! nc -z rabbitmq 5672; do
  sleep 0.25
done

echo "rabbitmq started"


exec "$@"