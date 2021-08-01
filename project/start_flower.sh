#!/bin/sh

worker_ready() {
    celery --app=app.main.celery inspect ping
}

until worker_ready; do
  echo 'Celery workers not available'
  sleep 0.25
done
echo 'Celery workers is available'

celery --app=app.main.celery \
        --broker="${CELERY_BROKER_URL}" \
        flower \
        --port=5555
