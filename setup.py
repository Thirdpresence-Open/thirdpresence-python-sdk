#!/usr/bin/env python
from setuptools import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='thirdpresence-sdk',
    version='1.0.3',
    description='This client library supports the official ThirdPresence API. '
                'Use it for implementing Python applications utilizing '
                'ThirdPresence',
    long_description=read("README.md"),
    author='ThirdPresence',
    url='http://wiki.thirdpresence.com',
    license='LGPL',
    py_modules=[
        'thirdpresence',
    ],
    install_requires = ["requests"],
)
