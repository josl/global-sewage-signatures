#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of global_sewage_signatures.
# https://github.com/josl/Global_Sewage_Signatures

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2016, Jose L. Bellod Cisneros & Kosai Al-Nakked
# <bellod.cisneros@gmail.com & kosai@cbs.dtu.dk>

# from global_sewage_signatures import MinHash as MH
import redis
from pkg_resources import resource_filename
# import numpy as np
import sys
import threading
import time
from bitarray import bitarray
from struct import *
import lupa
from lupa import LuaRuntime
import pickle


# Hostname comes from docker-compose.yml "depends_on" directive
redis_db = redis.StrictRedis(db=0, host='redis', port=6379)
dist = 0.2
sparse_matrix = []
hash_funcs = 100
keys = len(redis_db.keys())
module = 'global_sewage_signatures'
lua_file = 'pop_index.sparse.lua'

size = 4**16
a = bitarray(size)
a.setall(True)
a[45] = False

lua = LuaRuntime(unpack_returned_tuples=True)

# with open(resource_filename(module, 'coroutine.lua')) as lua_file:
#     # Load Lua script as a string
#     lua_code = lua_file.read()
#     # Lua script now can be called as a function called pop_index(KEY)
#     my_test = lua.eval(lua_code)
#     co = my_test.coroutine(4)
#     print(list(enumerate(co)))
# exit()


def worker(key):
    max_bytes = int(2**32 / 8)
    step = int(2**232 / 8)
    tot = redis_db.strlen(key) * 8
    pop = redis_db.bitcount(key)
    values = []
    found = 0

    if pop < (tot - pop):
        start = time.time()
        totals = 0
        myco = pop_index.coroutine(redis_db.get(key), pop)
        for i in myco:
            totals += 1
            estimated = (((time.time() - start) / totals)) * ((tot - pop) - totals) / (60)
            sys.stdout.write('Sparse: %s %s %.2f %.2f m.\r' % (i, pop, totals*100/pop, estimated))
        print(totals, pop)
    else:
        start = time.time()
        totals = 0
        myco = zeroes_index.coroutine(redis_db.get(key), tot - pop)
        for i in myco:
            totals += 1
            estimated = (((time.time() - start) / totals)) * ((tot - pop) - totals) / (60)
            sys.stdout.write('Dense: %s Totals: %s %.2f %.2f m.\r' % (i, tot - pop, totals*100/(tot - pop), estimated))
        print(totals, tot - pop, pop)
    with open(str(key) + '_file.pkl', 'wb') as out_file:
        pickle.dump(values, out_file, -1)


with open(resource_filename(module, lua_file)) as lua_file:
    # Load Lua script as a string
    lua_code = lua_file.read()
    # Lua script now can be called as a function called pop_index(KEY)
    pop_index = lua.eval(lua_code)
    lua_file = 'pop_index.dense.lua'
    with open(resource_filename(module, lua_file)) as lua_file:
        lua_code = lua_file.read()
        zeroes_index = lua.eval(lua_code)
        threads = []
        for key in redis_db.keys():
            t = threading.Thread(target=worker, args=(key,))
            threads.append(t)
            t.start()
            break

exit()

sparsed = []
for key in range(0, 85):
    population = redis_db.bitcount(key)
    sparsed.append(population*100/size)
    # print('%.2f' % (population*100/size))
redis_db = redis.StrictRedis(db=1, host='redis', port=6379)
for key, spar in enumerate(reversed(sorted(sparsed))):
    redis_db.get(key)
    print('%s: \t%.2f' % (redis_db.get(key), spar))
exit()

def worker(key):
    population = redis_db.bitcount(key)
    a = bitarray()
    a.frombytes(redis_db.get(key))
    index = 0
    ones = 0
    # sys.stdout.write('\n')
    start = time.time()
    for bit in a:
        if bit:
            redis_db.rpush(str(key) + '_index', index)
            ones += 1
            estimated = (((time.time() - start) / ones) * (population - ones)) / (60*60)
            sys.stdout.write('Thread: [%s] bit: %s out of %s (%.2f) %.2f hour\r' % (key, ones, population, 100*ones/population, estimated))
        index += 1

threads = []

for key in range(0, 85):
    t = threading.Thread(target=worker, args=(key,))
    threads.append(t)
    t.start()


exit()
for key in range(0, 85):
    step = 100
    total = 536870911

    total_bits = 4**16

    a = bitarray()
    b = bitarray(total_bits)
    b[total_bits - 1] = 1
    a.frombytes(redis_db.get('0'))
    print(a.length(), b.length())
    temp = []
    index = 0
    ones = 0
    start = time.time()
    for bit in a:
        if bit:
            ones += 1
            estimated = (((time.time() - start) / ones) * (population - ones)) / (60*60*24)
            sys.stdout.write('bit: %s out of %s (%.2f) %.2f days\r' % (ones, population, 100*ones/population, estimated))
            temp.append(index)
        index += 1
    break
exit()

with open(resource_filename(module, lua_file)) as lua_file:
    # Load Lua script as a string
    lua = lua_file.read()
    # Lua script now can be called as a function called pop_index(KEY)
    pop_index = redis_db.register_script(lua)
    start = time.time()
    ones = 0
    for i in range(total_bits - 1, -1, -1):
        bit_i = pop_index(keys=['0'], args=[i, total_bits - 1])
        if bit_i:
            ones += 1
            estimated = (((time.time() - start) / ones) * (population - ones)) / (60*60*24)
            sys.stdout.write('bit: %s out of %s (%.2f) %.2f days\r' % (ones, population, 100*ones/population, estimated))
exit()

# bit: 2463913 out of 3027838872 (0.08) 20998914.02 days # Slow........
start = time.time()
ones = 0
for start in range(0, total):
    bit_index = redis_db.bitpos('0', 1, start)
    ones += 1
    estimated = (((time.time() - start) / ones) * (population - ones)) / (60*60*24)
    sys.stdout.write('bit: %s out of %s (%.2f) %.2f days\r' % (ones, population, 100*ones/population, estimated))

exit()

with open(resource_filename(module, lua_file)) as lua_file:
    # Load Lua script as a string
    lua = lua_file.read()
    # Lua script now can be called as a function called pop_index(KEY)
    pop_index = redis_db.register_script(lua)
    key = '0'
    start = 0
    end = -1
    step = 100
    total = 536870911
    pipe = redis_db.pipeline()
    # pop_index(keys=[key], args=[start, end], client=pipe)
    # pop_index(keys=[key], args=[1, -1], client=pipe)
    # for i in pipe.execute():
    #     print(i)
    for start in range(0, total, step):
        # value = redis_db.bitpos(key, 1, start, start + end)
        # while value != -1:
        #     # Inspecting remaining bits
        #     for bit in range(value + 1, 7):
        #         other_ones = pop_index(keys=['0'], args=[bit])
        #         if other_ones[1] == 1 then
        #             byte_table[total_count] = start_byte * 8 + i
        #             total_count = total_count + 1
        #         end
        sys.stdout.write('%s out of total (%.2f)\r' % (start, start*100/total))
        pop_index(keys=[key], args=[start, start + step], client=pipe)
    for i in pipe.execute():
        population = redis_db.bitcount('0')
        try:
            print(len(i), population)
        except:
            print(i, population)
        # start += 1
    # value = pop_index(keys=[key], args=[start, end])
    # while value != -1:
    #     print(value)
    #     start += 1
    #     value = pop_index(keys=[key], args=[start, end])
