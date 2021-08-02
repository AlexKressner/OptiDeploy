
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



## Serving your own model
Easy, just define your model in the [model.py](https://github.com/AlexKressner/OptiDeploy/blob/master/project/app/optimizer) file.









