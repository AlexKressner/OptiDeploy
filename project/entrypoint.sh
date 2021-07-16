#!/bin/sh

echo "Waiting for mongo..."

while ! nc -z mongodb 27017; do
  sleep 0.1
done

echo "Mongodb started"

exec "$@"