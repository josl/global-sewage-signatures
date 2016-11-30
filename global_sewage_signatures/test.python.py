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
import time
from bitarray import bitarray
from struct import *

# Hostname comes from docker-compose.yml "depends_on" directive
redis_db = redis.StrictRedis(db=3, host='redis', port=6379)
dist = 0.2
sparse_matrix = []
hash_funcs = 100
keys = len(redis_db.keys())


# size = 4**16
# a = bitarray(size)
# a.setall(True)
# a[45] = False
# redis_db.set('test5', a.tobytes())

def worker_dense(key):

    key = 'test5'
    print(key)
    byte_string = redis_db.get(key)
    bytes_read = 0
    bytes_to_unpack = 1
    # bytes_to_unpack = string.len(s)
    # if bytes_to_unpack > 32 then
    #      bytes_to_unpack = 1
    #  end
    #  max = string.len(s) / bytes_to_unpack
    max_bytes = len(byte_string)  / bytes_to_unpack
    tot_bits = max_bytes * 8
    tot = len(byte_string) * 8
    zeroes = 0
    positions = []
    total_bytes = 1
    negation = 2 ** (bytes_to_unpack * 8) - 1
    fmt = str(bytes_to_unpack) + 'B'
    pop = redis_db.bitcount(key)
    tot = len(byte_string) * 8
    start = time.time()
    print(bytes_read, max_bytes)
    while bytes_read < max_bytes:
        d = unpack_from(fmt, byte_string, bytes_read)
        bytes_read += (1 * bytes_to_unpack)
        d = negation - d[0]
        while d:
            tot -= 1
            # zeroes = zeroes + 1
            # Calculate position of 1
            # d_ones = d
            # inner_zeroes = 0
            # while not d_ones & 1:
            #     inner_zeroes += 1
            #     d_ones >>= 1
            # positions.append(((bytes_read - 1) * 8) - 1 - inner_zeroes)
            # estimated = (((time.time() - start) / len(positions)) * ((tot_bits - pop) - len(positions))) / (60*60)
            # sys.stdout.write('Thread: [%s] %s out of total (%s) %.2f hours\r' % (key, len(positions), tot_bits - pop, estimated))
            d &= d - 1

    print('\n',tot, pop)
# def worker_sparse(key):

threads = []
for key in range(0, 85):
    tot = redis_db.strlen(key) * 8
    pop = redis_db.bitcount(key)
    if pop < (tot - pop) and False:
        t = threading.Thread(target=worker_sparse, args=(key,))
    else:
        t = threading.Thread(target=worker_dense, args=(key,))
    threads.append(t)
    t.start()
    break
