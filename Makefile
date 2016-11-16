#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of global_sewage_signatures.
# https://github.com/josl/Global_Sewage_Signatures

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2016, Jose L. Bellod Cisneros & Kosai Al-Nakked
# <bellod.cisneros@gmail.com & kosai@cbs.dtu.dk>

# lists all available targets
list:
	@sh -c "$(MAKE) -p no_targets__ | awk -F':' '/^[a-zA-Z0-9][^\$$#\/\\t=]*:([^=]|$$)/ {split(\$$1,A,/ /);for(i in A)print A[i]}' | grep -v '__\$$' | grep -v 'make\[1\]' | grep -v 'Makefile' | sort"
# required for list
no_targets__:

# install all dependencies (do not forget to create a virtualenv first)
setup:
	@pip install -U -e .\[tests\]

# test your application (tests in the tests/ directory)
test: mongo_test redis_test unit

unit:
	@coverage run --branch `which nosetests` -vv --with-yanc -s tests/
	@coverage report -m --fail-under=80

# show coverage in html format
coverage-html: unit
	@coverage html

# get a redis instance up (localhost:4444)
redis: kill_redis
	redis-server ./redis.conf; sleep 1
	redis-cli -p 4444 info > /dev/null

# kill this redis instance (localhost:4444)
kill_redis:
	-redis-cli -p 4444 shutdown

# get a redis instance up for your unit tests (localhost:4448)
redis_test: kill_redis_test
	@redis-server ./redis.tests.conf; sleep 1
	@redis-cli -p 4448 info > /dev/null

# kill the test redis instance (localhost:4448)
kill_redis_test:
	@-redis-cli -p 4448 shutdown

# get a mongodb instance up (localhost:3333)
mongo: kill_mongo
	@mkdir -p /tmp/global_sewage_signatures/mongodata && mongod --dbpath /tmp/global_sewage_signatures/mongodata --logpath /tmp/global_sewage_signatures/mongolog --port 3333 --quiet &

# kill this mongodb instance (localhost:3333)
kill_mongo:
	@-ps aux | egrep -i 'mongod.+3333' | egrep -v egrep | awk '{ print $$2 }' | xargs kill -9

# clear all data in this mongodb instance (localhost: 3333)
clear_mongo:
	@rm -rf /tmp/global_sewage_signatures && mkdir -p /tmp/global_sewage_signatures/mongodata

# get a mongodb instance up for your unit tests (localhost:3334)
mongo_test: kill_mongo_test
	@rm -rf /tmp/global_sewage_signatures/mongotestdata && mkdir -p /tmp/global_sewage_signatures/mongotestdata
	@mongod --dbpath /tmp/global_sewage_signatures/mongotestdata --logpath /tmp/global_sewage_signatures/mongotestlog --port 3334 --quiet --fork
	@echo 'waiting for mongo...'
	@until mongo --port 3334 --eval "quit()"; do sleep 0.25; done > /dev/null 2> /dev/null

# kill the test mongodb instance (localhost: 3334)
kill_mongo_test:
	@-ps aux | egrep -i 'mongod.+3334' | egrep -v egrep | awk '{ print $$2 }' | xargs kill -9

# run tests against all supported python versions
tox:
	@tox

#docs:
	#@cd global_sewage_signatures/docs && make html && open _build/html/index.html
