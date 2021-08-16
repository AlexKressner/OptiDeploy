
## About The Project
**Serving mathematical optimization models as a web service made easy!** powered by SCIP, FastAPI, mongodb and Celery.

This repository contains a template for building a containerized web services which serves an optimization model build with [SCIP](https://www.scipopt.org/index.php#about), which is currently one of the fastest non-commercial solvers for mixed integer programming (MIP) and mixed integer nonlinear programming (MINLP). Using [FastAPI](https://fastapi.tiangolo.com) optimization models are served as a RESTful API. The backend is powered by mongodb and stores problem instances and solutions. Optimizations run as background tasks via [Celery](https://docs.celeryproject.org/en/stable/). A simple facility location problem is used as an example optimization model.



## Getting Started

Make sure [Docker](https://www.docker.com) and [Docker Compose](https://docs.docker.com/compose/install/) is installed.

1. Clone repo
  ```sh
    git clone https://github.com/AlexKressner/OptiDeploy
  ```
2. Change directory
  ```sh
    cd OptiDeploy
  ```

3. Build and launch with docker-compose
  ```sh
    docker-compose up -d --build
  ```

4. Visit http://localhost:8004/docs to see spec of RESTful API via OpenAPI

5. Visit http://localhost:5556 to see flower for monitoring and administrating celery cluster

6. Visit http://localhost:15672 and login (user=admin, password=admin) to see the RabbitMQ dashboard


## Deployment to DigitalOcean with docker swarm

1. Create an account on Docker Hub, if you don't already have one, and then log in:
  ```sh
    docker login
  ```
2. Build, tag and push the images to Docker Hub:
  ```sh
    docker build -t [your docker hub namespace]/optideploy_base:latest -f ./project/Dockerfile ./project
    docker build -t [your docker hub namespace]/optideploy_db:latest -f ./project/db/Dockerfile ./project/db

    docker push [your docker hub namespace]/optideploy_base:latest
    docker push [your docker hub namespace]/optideploy_db:latest
  ```
3. Sign up for a DigitalOcean account (if you don’t already have one), and then generate an access token so you can access the DigitalOcean API.

4. Add your token:
  ```sh
  export DIGITAL_OCEAN_ACCESS_TOKEN=[your_digital_ocean_token]
  ```
5. Configure deployment setting (number of nodes, node size, etc., for details see https://slugs.do-api.dev) in deploy.sh and run deploy script:
  ```sh 
  sh deploy.sh
  ```
6. Fetch IP adress from terminal and test the endpoints:
  - http://[your ip adress]:8004/docs to see spec of RESTful API via OpenAPI
  - http://[your ip adress]:5556 to see flower for monitoring and administrating celery cluster
  - http://[your ip adress]:15672 and login (user=admin, password=admin) to see the RabbitMQ dashboard

7. Bring down the stack and remove the nodes:
  ```sh 
  sh remove.sh
  ```

## Serving your own model
Easy, just define your model in the [model.py](https://github.com/AlexKressner/OptiDeploy/blob/master/project/app/optimizer) file.









