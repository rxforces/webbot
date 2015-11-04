FROM ubuntu:trusty
MAINTAINER RXForces <rxforces@gmail.com>
RUN apt-get update && \
    apt-get install -y python python3 python-pip python3-pip python-dev python3-dev && \
    apt-get clean
RUN pip install --upgrade dogapi requests mandrill prettytable
RUN apt-get install -y python-mysql.connector
