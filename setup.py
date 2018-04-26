#!/usr/bin/env python

import os
import runpy

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

metadata_filename = "releasemaker/metadata.py"
metadata = runpy.run_path(metadata_filename)

setup(
    name='releasemaker',
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

