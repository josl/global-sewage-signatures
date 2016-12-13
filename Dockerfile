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
    vim \
    libluajit-5.1-dev \
    liblua5.1-dev \
    unzip \
    sudo \
    wget \
    lua5.1-dev \
    lua5.1 \
    unzip \
    luajit \
    make \
    gcc \
    libc-dev \
    libcurl4-openssl-dev \
    libevent-dev git \
    libevent-2.0-5 \
    libevent-core-2.0-5 \
    libevent-extra-2.0-5 \
    libevent-openssl-2.0-5 \
    libcurl3 \
    cmake \
    g++ \
    bison \
    libncurses5-dev \
    libssl-dev \
 && rm -rf /var/lib/apt/lists/*


WORKDIR /usr/app/src

RUN wget http://luarocks.org/releases/luarocks-2.4.0.tar.gz
RUN tar xzf luarocks-2.4.0.tar.gz && cd luarocks-2.4.0 && ./configure && make build && make install
RUN rm -rf luarocks-2.4.0.tar.gz

# RUN apt-get -y remove g++ bison libncurses5-dev lua5.1-dev libc-dev libssl-dev libcurl4-openssl-dev libevent-dev unzip cmake make gcc binutils libc-dev-bin git && apt-get -y autoremove && rm -rf /usr/local/mysql/lib/*.a /var/lib/apt/lists/*
# RUN cd && apt-get update && apt-get install -y wget lua5.1-dev lua5.1 unzip luajit make gcc libc-dev libcurl4-openssl-dev libevent-dev git libevent-2.0-5 libevent-core-2.0-5 libevent-extra-2.0-5 libevent-openssl-2.0-5 libcurl3 cmake g++ bison libncurses5-dev libssl-dev && rm -rf luarocks-2.4.0.tar.gz && wget http://luarocks.org/releases/luarocks-2.4.0.tar.gz && tar xzf luarocks-2.4.0.tar.gz && cd luarocks-2.4.0 && ./configure && make build && make install && cd .. && rm -rf luarocks-2.4.0* && wget https://github.com/MariaDB/server/archive/mariadb-5.5.48.tar.gz && tar xzf mariadb-5.5.48.tar.gz && cd server-mariadb-5.5.48 && cmake . && cd libmysql && make install && cd ../include && make install && cd && rm -rf mariadb-5.5.48.tar.gz server-mariadb-5.5.48 && luarocks install luafan MARIADB_DIR=/usr/local/mysql && apt-get -y remove g++ bison libncurses5-dev lua5.1-dev libc-dev libssl-dev libcurl4-openssl-dev libevent-dev unzip cmake make gcc binutils libc-dev-bin git && apt-get -y autoremove && rm -rf /usr/local/mysql/lib/*.a /var/lib/apt/lists/*


# RUN wget http://www.lua.org/ftp/lua-5.1.5.tar.gz
# RUN tar zxf lua-5.1.5.tar.gz
# WORKDIR /usr/src/lua-5.1.5
# RUN make linux test && make install
# ENV LD_LIBRARY_PATH=/usr/include/lua5.1/:$LD_LIBRARY_PATH
#
#
# WORKDIR /usr/src
#
# RUN wget http://luajit.org/download/LuaJIT-2.0.4.tar.gz
# RUN tar zxf LuaJIT-2.0.4.tar.gz
# WORKDIR /usr/src/LuaJIT-2.0.4
# RUN make && make install
# # RUN ln -s /usr/local/bin/luajit /usr/local/bin/lua
#
# WORKDIR /usr/src
# RUN wget http://luarocks.github.io/luarocks/releases/luarocks-2.4.1.tar.gz
# RUN tar zxf luarocks-2.4.1.tar.gz
# WORKDIR /usr/src/luarocks-2.4.1
# RUN ./configure --with-lua=/usr/local
# RUN make build
# RUN make install

# WORKDIR /usr/src
# RUN wget http://www.inf.puc-rio.br/~roberto/struct/struct-0.2.tar.gz
# RUN tar zxf struct-0.2.tar.gz
# WORKDIR /usr/src/struct-0.2
# RUN make -f makefile

WORKDIR /usr/src

COPY . /usr/src
RUN make setup
