#!/usr/bin/env python

import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

REQUIREMENTS = []

setup(
    name='pytic80',
    version='0.0.1',
    description='Python library for reading .tic files',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Robert Miles',
    author_email='khuxkm@tilde.team',
    url='https://github.com/MineRobber9000/pytic',
    license="MIT",
    install_requires=REQUIREMENTS,
    keywords=[],
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
    ]
)
