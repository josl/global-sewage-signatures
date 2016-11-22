#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of global_sewage_signatures.
# https://github.com/josl/Global_Sewage_Signatures

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2016, Jose L. Bellod Cisneros & Kosai Al-Nakked
# <bellod.cisneros@gmail.com & kosai@cbs.dtu.dk>

from . import MinHash as MH
from . import redis_db as rd

# Extract keys from redis db and create MinHash using Lua scripting
lua = """
    local value = redis.call('GET', KEYS[1])
    value = tonumber(value)
    return value * ARGV[1]
"""
distance = 0.2
sparse_matrix =
hash_functions = 100

# Dataset contains 85 x 4^16 datapoints

mh = Mh.MinHash(dist, sparse_matrix, k_permutations)
