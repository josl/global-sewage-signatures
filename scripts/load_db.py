#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of global_sewage_signatures.
# https://github.com/josl/Global_Sewage_Signatures

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2016, Jose L. Bellod Cisneros & Kosai Al-Nakked
# <bellod.cisneros@gmail.com & kosai@cbs.dtu.dk>

##
# This script loads bitarrays repressented ad bystring into a redis DB
##

import json
import redis
from bitarray import bitarray
from optparse import OptionParser
import os

r = redis.StrictRedis(db=0, host='redis', port=6379)

parser = OptionParser()
parser.add_option("-i", "--folder", dest="folder",
                  help="read fall files in FOLDER", metavar="FOLDER")
(options, args) = parser.parse_args()

folder = '/home/projects/cge/people/olund/projects/sewage/sewage5/'
bool_map = {False: '0', True: 1}
for root, directories, files in os.walk(folder):
    for file_name in files:
        if 'b16' not in file_name:
            continue
        # Join the two get absolute path.
        print(file_name)
        filepath = os.path.join(root, file_name)
        a = bitarray()
        with open(filepath, 'rb') as fh:
            a.fromfile(fh)
            r.set(file_name, a.tobytes())
