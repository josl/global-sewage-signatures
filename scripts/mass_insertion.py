#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of global_sewage_signatures.
# https://github.com/josl/Global_Sewage_Signatures

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2016, Jose L. Bellod Cisneros & Kosai Al-Nakked
# <bellod.cisneros@gmail.com & kosai@cbs.dtu.dk>

import json
import redis
from bitarray import bitarray
from optparse import OptionParser
import os

r = redis.StrictRedis(db=0)

# Source: https://gist.github.com/laserson/2689744


def gen_redis_proto(*args):
    proto = ''
    proto += '*' + str(len(args)) + '\r\n'
    for arg in args:
        proto += '$' + str(len(arg)) + '\r\n'
        proto += str(arg) + '\r\n'
    return proto

parser = OptionParser()
parser.add_option("-i", "--folder", dest="folder",
                  help="read fall files in FOLDER", metavar="FOLDER")
parser.add_option("-o", "--output", dest="output",
                  help="Redis Protocol output folder", metavar="OUTPUT")
(options, args) = parser.parse_args()

# folder = '/home/projects/cge/people/olund/projects/sewage/sewage5/'
with open(args.output, 'w') as fh:
    for root, directories, files in os.walk(args.folder):
        for filename in files:
            if 'b16' not in filename:
                continue
            # Join the two get absolute path.
            filepath = os.path.join(root, filename)
            a = bitarray()
            with open(filepath, 'rb') as fh:
                a.fromfile(fh)
                fh.write(gen_redis_proto('SET %s %s', % (file_name, a.tobytes())))
