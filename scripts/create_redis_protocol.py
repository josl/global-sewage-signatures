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
with open(options.output, 'w') as fhl:
    for root, directories, files in os.walk(options.folder):
        for file_name in files:
            if 'b16' not in file_name:
                continue
            print(file_name)
            # Join the two get absolute path.
            file_path = os.path.join(root, file_name)
            a = bitarray()
            with open(file_path, 'rb') as fh:
                a.fromfile(fh)
                fhl.write(gen_redis_proto('SET %s %s' % (file_name, a.tobytes())))
