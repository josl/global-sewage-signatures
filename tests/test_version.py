#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of global_sewage_signatures.
# https://github.com/josl/Global_Sewage_Signatures

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2016, Jose L. Bellod Cisneros & Kosai Al-Nakked
# <bellod.cisneros@gmail.com & kosai@cbs.dtu.dk>

from preggy import expect

from global_sewage_signatures import __version__
from tests.base import TestCase


class VersionTestCase(TestCase):

    def test_has_proper_version(self):
        expect(__version__).to_equal('0.1.0')
