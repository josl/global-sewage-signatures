#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of global_sewage_signatures.
# https://github.com/josl/Global_Sewage_Signatures

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2016, Jose L. Bellod Cisneros & Kosai Al-Nakked
# <bellod.cisneros@gmail.com & kosai@cbs.dtu.dk>

##
# This script creates an index of all (file names) documents and stores it in
# a redis database. A the same time it renames the keys presented in the
# database to follow a numerical pattern
##

import redis

r = redis.StrictRedis(db=0, host='redis', port=6379)
rw = redis.StrictRedis(db=1, host='redis', port=6379)

for index, key in enumerate(r.keys()):
    rw.set(index, key)
    r.rename(key, index)
