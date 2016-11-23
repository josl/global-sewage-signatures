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

class MinHashRedis(MH.MinHash):

    def __init__(self, dist, hash_funcs, documents, features, redis_db):
        super(self.__class__, self).__init__(dist, [], k_permutations)
        self.dimensions = features
        self.n_points = documents
        self.redis = redis_db

    # def redis_key_indices(self, key):
    #     indices = []
    #     start = 0
    #     end = 0
    #     while (zeroes=(redis_db.bitpos(key, 0, start, end) != -1)):
    #         # Append indices of ones (all before the first zero)
    #         indices.append(range(start, zeroes - 1))
    #         # Update start/end
    #         start = zeroes

    def createMinHash(self):
        for col_j in range(0, self.n_points):
            for sign_i, hash_func in enumerate(self.hash_permutations):
                for row_i in self.redis_key_indices(col_j):
                # for row_i in self.sparse_matrix[col_j].indices:
                    hash_row = hash_func(row_i)
                    if hash_row < self.signatures[col_j][sign_i]:
                        self.signatures[col_j][sign_i] = hash_row

# Hostname comes from docker-compose.yml "depends_on" directive
redis_db = redis.StrictRedis(db=0, host='redis', port=6379)

redis_db_test = redis.StrictRedis(db=3, host='redis', port=6379)

# Extract keys from redis db and create MinHash using Lua scripting
# lua = """
#     local index = 0
#
#
#     local value = redis.call('BITFIELD', KEYS[1], 'GET', 'u1', index)
#      BITFIELD test GET u1 0
#     for bit in
#     value = tonumber(value)
#     return value * ARGV[1]
# """

with open(resource_filename('global_sewage_signatures', 'pop_index.lua')) as lua_f:
    lua = lua_f.read()
    pop_index = redis_db_test.register_script(lua)


print(pop_index(keys=['test']))

# Dataset contains 85 x 4^16 datapoints.
#
# MinHash class expects a sparse_matrix containing indexes for each of the documents
#

distance = 0.2
sparse_matrix = []
hash_functions = 100

# mh = Mh.MinHash(dist, sparse_matrix, k_permutations)
