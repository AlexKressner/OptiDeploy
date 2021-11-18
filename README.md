
## About The Project
**Serving mathematical optimization models as a web service made easy!** powered by FastAPI, mongodb and Celery.

This repository contains a template for building a containerized web services which serves an optimization model build with [SCIP](https://www.scipopt.org/index.php#about) as an example. SCIP is currently one of the fastest non-commercial solvers for mixed integer programming (MIP) and mixed integer nonlinear programming (MINLP). Please note that the template is flexible enough to integrate other solvers and customized algorithms with minor adjustments and is not limited to SCIP. Using [FastAPI](https://fastapi.tiangolo.com), optimization models are served as a RESTful API. The backend is powered by [mongoDB](https://www.mongodb.com/de-de) and stores problem instances and solutions. Optimizations run as background tasks via [Celery](https://docs.celeryproject.org/en/stable/) using [RabbitMQ](https://www.rabbitmq.com) as broker and [redis](https://redis.io) as (intermediate) result backend. Professional log-management is realized with [Papertrail](https://papertrailapp.com). A simple facility location problem is used as an example optimization model.

Hopefully, this template helps people to be faster going from an optimization model on a local machine to a simple optimization web service that can be plugged in existing or new applications.


## Architectural Overview
<img src="https://user-images.githubusercontent.com/25706472/141779451-1a9b8ce9-0839-4a4d-b670-8d68c63f3f07.png">

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
2. Add your Docker Hub namespace:
  ```sh
    export DOCKERHUB_NAMESPACE=[your_dockerhub_namespace]
  ```
3. Run the init script to build and push the images to Docker Hub:
  ```sh
    source init_images.sh
  ```
4. Sign up for a DigitalOcean account (if you don’t already have one), and then generate an access token so you can access the DigitalOcean API.

5. Add your token:
  ```sh
    export DIGITAL_OCEAN_ACCESS_TOKEN=[your_digital_ocean_token]
  ``` 
6. Sign up for Papertrail with a free plan and add the service "app log files" (LINUX/UNIX) for professional Log-management. You will get a host and port (HOST.papertrailapp.com:PORT) which you should (permanently) add as an environment variable on your machine.
  ```sh
    export PAPERTRAIL_URL=HOST.papertrailapp.com:PORT
  ```
7. Configure deployment setting (number of nodes, node size, etc., for details see https://slugs.do-api.dev) in deploy.sh and docker-compose-swarm.yml (e.g. replicas). Afterwards run deploy script:
  ```sh 
    sh deploy.sh
  ```
8. Fetch IP adress from terminal and test the endpoints. It might take a minute until everything is setup and running on the server side.
  - [http://[your ip adress]:8004/docs](http://your_ip_adress:8004/docs) to see spec of RESTful API via OpenAPI
  - [http://[your ip adress]:5556](http://your_ip_adress:5556) to see flower for monitoring and administrating celery cluster
  - [http://[your ip adress]:15672](http://your_ip_adress:15672) and login (user=admin, password=admin) to see the RabbitMQ dashboard

9. Bring down the stack and remove the nodes:
  ```sh 
    sh remove.sh
  ```


## Continuous Integraion and Delivery with Github Actions
CI/CD workflows are implemented via [Github Actions](https://docs.github.com/en/actions). The branching workflow follows the so called ["Git Flow"](https://nvie.com/posts/a-successful-git-branching-model/) model. There are two branches with infinite lifetime: ```master``` which contains production code and ```develop``` which contains pre-production code and is merged to ```master``` when finished. CI runs for ```develop``` and ```master```. CD runs for ```master``` only. Feel free to use additional supporting branches (```feature```,```hotfix```, etc.). Deployments are done with zero downtime by using docker swarm's internal update mechanisms.


## Setting up CI/CD
1. ssh in the remote machine ("node-1") which is your swarm manager node:
  ```sh
    docker-machine ssh node-1
  ```

2. Generate private and public ssh keys - do not enter a passphrase:
  ```sh
    ssh-keygen
  ```

3. Copy public key to authorized keys:
  ```sh
    cat .ssh/id_rsa.pub >> .ssh/authorized_keys
  ```

4. Copy private key
  ```sh
    cat .ssh/id_rsa
  ````

5. Add secrets on github
  - PRIVATE_KEY: your private ssh key copied from the manager node
  - SERVER_IPV4: ip address of the manager node
  - PAPERTRAIL_URL: your papertrail url
  - DOCKERHUB_NAMESPACE: your dockerhub namespace
  - DOCKERHUB_ACCESS_TOKEN: your dockerhub access token to push and pull images
  - DIGITAL_OCEAN_ACCESS_TOKEN: your digitalocean access token to access the droplets



## Serving your own model
Easy, just do the following:
1. Define all the relevant sets and parameters of your problem as a pydantic model in [data.py](https://github.com/AlexKressner/OptiDeploy/blob/master/project/app/models/data.py). This model will also serve to validate data send
when placing a problem instance.
2. To control the behavior of your solver define another model in the [solver_parameters.py](https://github.com/AlexKressner/OptiDeploy/blob/master/project/app/optimizer/solver_parameters.py). This model will also be used to check solver settings sent via the API.
3. Finally, implement your solver in [solver.py](https://github.com/AlexKressner/OptiDeploy/blob/master/project/app/optimizer/solver.py).