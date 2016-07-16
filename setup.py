#!/usr/bin/env python

import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

metadata = {}
execfile("releasemaker/metadata.py", metadata)

setup(
    name='xcode_releasemaker',
    version=metadata['__version__'],
    license=metadata['__license__'],
    description="Build tool to create releases in GitHub.",
    author=metadata['__author__'],
    author_email=metadata['__email__'],
    url="http://lionheartsw.com/",
    packages=[
        'releasemaker',
    ],
    scripts=[
        'bin/releasemaker',
    ],
)

