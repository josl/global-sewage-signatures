#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of global_sewage_signatures.
# https://github.com/josl/Global_Sewage_Signatures

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2016, Jose L. Bellod Cisneros & Kosai Al-Nakked
# <bellod.cisneros@gmail.com & kosai@cbs.dtu.dk>

from setuptools import setup, find_packages
from global_sewage_signatures import __version__

tests_require = [
    'mock',
    'nose',
    'coverage',
    'yanc',
    'preggy',
    'tox',
    'ipdb',
    'coveralls',
    'sphinx',
]

setup(
    name='global_sewage_signatures',
    version=__version__,
    description='Grouping of global sewage samples based on DNA signatures',
    long_description='''
        Grouping of global sewage samples based on DNA signatures
    ''',
    keywords='DNA redis sequencing bioinformatics metagenomics',
    author='Jose L. Bellod Cisneros & Kosai Al-Nakked',
    author_email='bellod.cisneros@gmail.com & kosai@cbs.dtu.dk',
    url='https://github.com/josl/Global_Sewage_Signatures',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    install_requires=[
        # add your dependencies here
        # remember to use 'package-name>=x.y.z,<x.y+1.0' notation (this way you
        # get bugfixes)
        'redis>=2.10.5,<2.11',
        'numpy',
        'pyspark',
        'bitarray'
        'scipy',
        'cython'
    ],
    extras_require={
        'tests': tests_require,
    },
    entry_points={
        'console_scripts': [
            # add cli scripts here in this form:
            # 'global_sewage_signatures=global_sewage_signatures.cli:main',
        ],
    },
)
