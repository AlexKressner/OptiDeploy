# pull official base image
FROM python:3.9.2-slim-buster

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc\
  #install SCIP dependencies
  && apt-get -y install \
              libblas3 libboost-program-options1.67.0 \
              libcliquer1 libgfortran5 \
              libgmpxx4ldbl libgsl23 \
              libgslcblas0 liblapack3\
              libopenblas-base libtbb2\
  && apt-get clean

COPY ./SCIPOptSuite-7.0.3-Linux-debian.deb .
RUN dpkg -i SCIPOptSuite-7.0.3-Linux-debian.deb \
    && rm SCIPOptSuite-7.0.3-Linux-debian.deb


# install python dependencies
RUN pip install --upgrade pip
RUN pip install pyscipopt==3.2.1
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# add app
COPY . .

# add entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod +x /usr/src/app/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
