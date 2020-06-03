# setup.py: script to setup gggolfclient
#!/usr/bin/env python
# 
# (C) Copyright 2018-2019 Yu-Yueh Liu
import os.path
import re
import sys

from setuptools import setup, find_packages

import os
thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
install_requires = [] # Examples: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()
setup(
    name = 'gggolfclient',
    version = '0.1.0',
    packages = ['gggolfclient'],
    entry_points = {
        'console_scripts': [
            'gggolfclient = gggolfclient.__main__:main'
        ]
    },
    install_requires=install_requires)