#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of global_sewage_signatures.
# https://github.com/josl/Global_Sewage_Signatures

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2016, Jose L. Bellod Cisneros & Kosai Al-Nakked
# <bellod.cisneros@gmail.com & kosai@cbs.dtu.dk>

FROM python:latest
MAINTAINER Jose L. Bellod Cisneros & Kosai Al-Nakked <bellod.cisneros@gmail.com & kosai@cbs.dtu.dk>


RUN apt-get update && apt-get install -y -qq --no-install-recommends \
    aufs-tools \
    automake \
    build-essential \
    curl \
    dpkg-sig \
    libcap-dev \
    libsqlite3-dev \
    reprepro \
 && rm -rf /var/lib/apt/lists/*



WORKDIR /home/docker/app

COPY . /home/docker/app
RUN make setup

RUN groupadd -g 1000 docker
RUN useradd -u 1000 -r -g docker -d /home/docker -s /bin/bash -c "HTTP Server User" docker

RUN mkdir -p /home/docker
RUN chown -R docker:docker /home/docker


ENV HOME /home/docker
USER docker
EXPOSE 4444

ENTRYPOINT [ "redis-server", "./redis.conf" ]
