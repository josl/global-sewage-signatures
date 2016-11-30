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
import sys
import threading


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

    def worker():


    def createMinHash(self):
        for col_j in range(0, self.n_points):
            print('Pushing document... ', col_j)
            for sign_i, hash_func in enumerate(self.hash_permutations):
                key = col_j
                start = 0
                end = -1
                pipe = self.redis.pipeline()
                step = 100

                # for start in range(0, 536870911, step):
                #     sys.stdout.write(str(key) + ' ' + str(start) + '\r')
                #     self.pop_index(keys=[key], args=[start, start + step], client=pipe)
                #     # start += 1
                # for matrix_ones in pipe.execute():
                #     if matrix_ones == -1:
                #         break
                #     sys.stdout.write(' '.join([str(i) for i in matrix_ones]) + '\r')
                #     for row_one in matrix_ones:
                #         hash_row = hash_func(row_one)
                #         if hash_row < self.signatures[col_j][sign_i]:
                #             self.signatures[col_j][sign_i] = hash_row

                threads = []
                t = threading.Thread(target=worker, args=(i,))
                threads.append(t)
                t.start()
                population = self.redis.bitcount(key)
                matrix_ones = self.pop_index(keys=[key], args=[start, end])
                while matrix_ones != -1:
                    # sys.stdout.write(' '.join([str(i) for i in matrix_ones]) + '\r')
                    for row_one in matrix_ones:
                        sys.stdout.write('%s out of %s (%.2f)' % (row_one, population, row_one*100/population) + '\r')
                        hash_row = hash_func(row_one)
                        if hash_row < self.signatures[col_j][sign_i]:
                            self.signatures[col_j][sign_i] = hash_row
                    start += 1
                    matrix_ones = self.pop_index(keys=[key], args=[start, end])

# Hostname comes from docker-compose.yml "depends_on" directive
redis_db = redis.StrictRedis(db=0, host='redis', port=6379)

dist = 0.2
sparse_matrix = []
hash_funcs = 100
keys = len(redis_db.keys())
module = 'global_sewage_signatures'
lua_file = 'pop_index.test.lua'

# with open(resource_filename(module, lua_file)) as lua_file:
#     # Load Lua script as a string
#     lua = lua_file.read()
#     # Lua script now can be called as a function called pop_index(KEY)
#     pop_index = redis_db.register_script(lua)
#     key = 'test'
#     start = 0
#     end = -1
#     value = pop_index(keys=[key], args=[start, end])
#     while value != -1:
#         print(value)
#         start += 1
#         value = pop_index(keys=[key], args=[start, end])

# Dataset contains 85 x 4^16 datapoints.
mh = MinHashRedis(dist, hash_funcs, keys, 4**16, redis_db, module, lua_file)
mh.createMinHash()

# Save signature matrix to Redis, DB[4]
redis_db_signs = redis.StrictRedis(db=4, host='redis', port=6379)
for row, signatures in enumerate(mh.signatures):
    redis_db_signs.set(row, signatures)
