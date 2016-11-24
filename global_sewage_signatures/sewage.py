#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of global_sewage_signatures.
# https://github.com/josl/Global_Sewage_Signatures

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2016, Jose L. Bellod Cisneros & Kosai Al-Nakked
# <bellod.cisneros@gmail.com & kosai@cbs.dtu.dk>

from global_sewage_signatures import MinHash as MH
import redis
from pkg_resources import resource_filename
import numpy as np


class MinHashRedis(MH.MinHash):

    def __init__(self, dist, h_funcs, docs, features, redis_db, module, lua_f):
        # Dummy sparse set so MinHash won't complain
        empty_sparse = np.matrix('0; 0')
        super(self.__class__, self).__init__(dist, empty_sparse, h_funcs)
        self.dimensions = features
        self.n_points = docs
        self.redis = redis_db
        with open(resource_filename(module, lua_f)) as lua_file:
            # Load Lua script as a string
            lua = lua_file.read()
            # Lua script now can be called as a function called pop_index(KEY)
            self.pop_index = self.redis.register_script(lua)

    def createMinHash(self):
        for col_j in range(0, self.n_points):
            print('Pushing document... ', col_j)
            for sign_i, hash_func in enumerate(self.hash_permutations):
                for row_i in self.pop_index(keys=[col_j]):
                    print(row_i)
                    hash_row = hash_func(row_i)
                    if hash_row < self.signatures[col_j][sign_i]:
                        self.signatures[col_j][sign_i] = hash_row

# Hostname comes from docker-compose.yml "depends_on" directive
redis_db = redis.StrictRedis(db=0, host='redis', port=6379)

dist = 0.2
sparse_matrix = []
hash_funcs = 100
keys = len(redis_db.keys())
module = 'global_sewage_signatures'
lua_file = 'pop_index.lua'

with open(resource_filename(module, lua_file)) as lua_file:
    # Load Lua script as a string
    lua = lua_file.read()
    # Lua script now can be called as a function called pop_index(KEY)
    pop_index = redis_db.register_script(lua)
    pop_index(keys=[0])
# Dataset contains 85 x 4^16 datapoints.
# mh = MinHashRedis(dist, hash_funcs, keys, 4**16, redis_db, module, lua_file)
# mh.createMinHash()

# Save signature matrix to Redis, DB[4]
# redis_db_signs = redis.StrictRedis(db=4, host='redis', port=6379)
# for row, signatures in enumerate(mh.signatures):
#     redis_db_signs.set(row, signatures)
