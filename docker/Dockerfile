# Dockerfile has three Arguments: base, tag, branch
# base - base image (default: ubuntu, optional: debian)
# tag - tag for base mage (default: 20.04)
# branch - user repository branch to clone (default: master)
#
# To build the image:
# $ docker build -t <dockerhub_user>/<dockerhub_repo> --build-arg arg=value .
# or using default args:
# $ docker build -t <dockerhub_user>/<dockerhub_repo> .

# set the base image. default is ubuntu, optional debian
ARG base=ubuntu
# set the tag (e.g. latest, 20.04 for ubuntu; stable, stable-slim : for debian)
ARG tag=20.04

# Base image, e.g. debian:stable or ubuntu:bionic
FROM ${base}:${tag}

LABEL maintainer='XXX'
# o3webapp-be (backend) as a component of the Ozone assessment service

# What user branch to clone (!)
ARG branch=master

# Install system updates and tools
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
# Install system updates and tools
        git \
        nano \
        procps \
# Install system updates and tools
        python3-setuptools \
        python3-pip \
        python3-wheel && \
# Clean up & back to dialog front end
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*
ENV DEBIAN_FRONTEND=dialog
WORKDIR /srv

# Install user app:
RUN git clone --depth 1 -b $branch https://git.scc.kit.edu/synergy.o3as/o3webapp-be.git && \
# Install o3webapp-be
    cd o3webapp-be && \
    pip3 install --no-cache-dir -e . && \
# Clean up
    rm -rf /root/.cache/pip/* && \
    rm -rf /tmp/*

WORKDIR /srv/o3webapp-be

# Set environments
ENV FLASK_APP o3webapp_be.back_end.py
ENV LANG C.UTF-8

# Expose the port
EXPOSE 5000

# Start default script
CMD ["flask", "run", "--host", "0.0.0.0"]
