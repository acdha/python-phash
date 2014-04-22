#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='phash',
    version='0.1.0',
    description='ctypes interface to libphash',
    long_description=readme + '\n\n' + history,
    author='Chris Adams',
    author_email='chris@improbable.org',
    url='https://github.com/acdha/python-phash',
    packages=[
        'phash',
    ],
    package_dir={'phash': 'phash'},
    scripts=['scripts/compare-images.py'],
    include_package_data=True,
    install_requires=[
        'more-itertools',
    ],
    license="BSD",
    zip_safe=False,
    keywords='phash',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)