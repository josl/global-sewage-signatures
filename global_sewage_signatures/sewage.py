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
import lupa
from lupa import LuaRuntime
import time
import numpy as np
import math



class MinHashRedis(MH.MinHash):

    def __init__(self, dist, h_funcs, docs, features, redis_db):
        # Dummy sparse set so MinHash won't complain
        empty_sparse = np.matrix('0; 0')
        super(self.__class__, self).__init__(dist, empty_sparse, h_funcs, len(docs), features)
        self.dimensions = features
        self.n_points = len(docs)
        self.redis = redis_db
        self.documents = dict((key, file)
                              for key, file in list(enumerate(docs)))
        self.signatures = [
            np.array([math.inf for i in range(0, h_funcs)])
            for j in range(0, self.n_points)
        ]
        # Loading Lua Scripts
        with open(resource_filename(module, 'pop_index.sparse.lua')) as lua_f:
            self.lua_sparse = lua_f.read()
        with open(resource_filename(module, 'pop_index.dense.lua')) as lua_f:
            self.lua_dense = lua_f.read()

    def worker(self, key, signature_row, pop_index, zeroes_index):
        redis_key = self.documents[key]
        zeroes = False

        # Total number of bits
        tot = self.redis.strlen(redis_key) * 8
        # Number of bits set to 1
        pop = self.redis.bitcount(redis_key)
        # Number of bits set to zero
        zeros = tot - pop
        # Extracting indices...
        if pop < (tot - pop):
            # Sparse array.
            indices = pop_index.coroutine(bit_string, pop, start_byte)
        else:
            # Dense array. Flag working with zero-type indexes
            zeroes = True
            indices = zeroes_index.coroutine(
                bit_string, tot - pop, start_byte)
        # Variables to calculate estimated time remaining and progress
        totals = 0
        estimated = 0.0
        zero_start = 0
        start = time.time()
        for row_i in indices:
            # We loop over values returned by yield in Lua coroutine
            totals += 1
            if zeroes:
                # We are dealing with zeroes. We create a range with zeroes as
                # boundaries
                for row_i_ones in range(zero_start, row_i):
                    estimated = (((time.time() - start) / totals)
                                        ) * ((tot - pop) - totals) / (60)
                    sys.stdout.write('ThreadD [%s] %s  %s %s %.2f %.2f m.\r' % (
                        key, totals, zeros, totals * 100 / zeros, estimated))
                    # We calculate all permutations for this index using
                    # Universal Hashing previously created.
                    for sign_i, hash_func in enumerate(self.hash_permutations):
                        hash_row = hash_func(row_i_ones)
                        # Comparison with the signature matrix and update.
                        if hash_row < signature_row[sign_i]:
                            signature_row[sign_i] = hash_row
                # Increasing of the zero boundary to avoid it in next iteration
                zero_start = row_i + 1
            else:
                # Sparse array. Indexes returned are ones.
                estimated = (
                    ((time.time() - start) / totals)) * ((pop) - totals) / (60)
                sys.stdout.write('ThreadS [%s] %s %s %.2f %.2f m.\r' % (
                    key, totals, pop, totals * 100 / pop, estimated))
                for sign_i, hash_func in enumerate(self.hash_permutations):
                    hash_row = hash_func(row_i)
                    if hash_row < signature_row[sign_i]:
                        signature_row[sign_i] = hash_row
        start = time.time()
        # In the case of Dense array check if last zero index is last bit
        if zero_start < (tot - 1) and zeroes:
            for row_i_ones in range(zero_start, tot - 1):
                totals += 1
                estimated = (
                    ((time.time() - start) / totals)) * ((tot - pop) - totals) / (60)
                sys.stdout.write('ThreadDE [%s] %s %s %.2f %.2f m.\r' % (
                    key, row_i_ones, pop, totals * 100 / pop, estimated))
                for sign_i, hash_func in enumerate(self.hash_permutations):
                    hash_row = hash_func(row_i_ones)
                    if hash_row < signature_row[sign_i]:
                        signature_row[sign_i] = hash_row

    def createMinHash(self):
        # We are working with a processor that has 28 cores.
        step = 28
        for start in range(0, self.n_points, step):
            threads = []
            if start > self.n_points:
                break
            for col_j in range(start, start + step):
                if col_j >= self.n_points:
                    break
                lua = LuaRuntime(unpack_returned_tuples=True, encoding=None)
                pop_index = lua.eval(self.lua_sparse)
                zeroes_index = lua.eval(self.lua_dense)
                t = threading.Thread(target=self.worker, args=(
                    col_j, self.signatures[col_j], pop_index, zeroes_index))
                threads.append(t)
            for t in threads:
                t.start()
            for t in threads:
                t.join()


# Hostname comes from docker-compose.yml "depends_on" directive
redis_db = redis.StrictRedis(db=0, host='redis', port=6379)

dist = 0.2
hash_funcs = 100
keys = redis_db.keys()

# Dataset contains 85 x 4^16 datapoints.
mh = MinHashRedis(dist, hash_funcs, keys, 4**16, redis_db)
# Creating MinHash
mh.createMinHash()
# Saving MinHash signatures in a different Redis DB for later use.
redis_db_signs = redis.StrictRedis(db=1, host='redis', port=6379)
for key, signatures in enumerate(mh.signatures):
    redis_db_signs.set(mh.documents[key], signatures)
