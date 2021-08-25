
## About The Project
**Serving mathematical optimization models as a web service made easy!** powered by SCIP, FastAPI, mongodb and Celery.

This repository contains a template for building a containerized web services which serves an optimization model build with [SCIP](https://www.scipopt.org/index.php#about) as an example. SCIP is currently one of the fastest non-commercial solvers for mixed integer programming (MIP) and mixed integer nonlinear programming (MINLP). Using [FastAPI](https://fastapi.tiangolo.com), optimization models are served as a RESTful API. The backend is powered by [mongoDB](https://www.mongodb.com/de-de) and stores problem instances and solutions. Optimizations run as background tasks via [Celery](https://docs.celeryproject.org/en/stable/) using [RabbitMQ](https://www.rabbitmq.com) as broker and [redis](https://redis.io) as (intermediate) result backend. A simple facility location problem is used as an example optimization model.

Hopefully, this template helps people to be faster going from an optimization model on a local machine to a simple optimization web service that can be plugged in existing or new applications.


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
5. Configure deployment setting (number of nodes, node size, etc., for details see https://slugs.do-api.dev) in deploy.sh and docker-compose-swarm.yml (e.g. replicas). Afterwards run deploy script:
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
Easy, just do the following:
1. Define all the relevant sets and parameters of your problem as a pydantic model in [data.py](https://github.com/AlexKressner/OptiDeploy/blob/master/project/app/optimizer/data.py). This model will also serve to validate data send
when placing a problem instance.
2. To control the behavior of your solve define another model in the [solver_parameters.py](https://github.com/AlexKressner/OptiDeploy/blob/master/project/app/optimizer/solver_parameters.py). This model will also be used to check solver settings sent via the API.
3. Finally, implement your solver in [solver.py](https://github.com/AlexKressner/OptiDeploy/blob/master/project/app/optimizer/solver_parameters.py).


## ToDo 
- Load balancer, security --> e.g. Traefik
- CI/CD --> e.g. github actions
- Monitoring --> prometheus (&grafana)









