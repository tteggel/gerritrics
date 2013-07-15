#!/usr/bin/env python

"""
Copyright (c) 2013, Thom Leggett.
License: MIT (see LICENSE for details)
"""

import sys

from setuptools import setup, find_packages

from activity.version import get_version

readme = open('README.rst').read()

long_description = readme

setup(
    name='activity',
    version=get_version(),
    description='OpenStack Activity is for visualising activity in OpenStack.',
    long_description=long_description,
    author='Thom Leggett',
    author_email='thom@tteggel.org',
    packages=['activity', 'activity.test'],
    test_suite='activity.test',
    tests_require=['nose',
                   'ws4py>=0.2.4',
                   'requests>=1.1.0',
                   'webtest>=1.4.3'],
    install_requires=['bottle==0.11.6',
                      'gevent==0.13.8',
                      'pymongo==2.5.2'],
    entry_points={
        'console_scripts': [
            'openstack-activity = activity.server:main',
        ]
    },
    zip_safe=False,
    include_package_data=True,
    classifiers=[
    ],
)