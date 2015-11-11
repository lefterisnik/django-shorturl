#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import shorturl

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = shorturl.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on github:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-shorturl',
    packages=['shorturl'],
    version=version,
    description='A django short URL app.',
    long_description=readme + '\n\n' + history,
    author='Lefteris Nikoltsios',
    author_email='lefteris.nikoltsios@gmail.com',
    url='https://github.com/lefterisnik/django-shorturl',
    include_package_data=True,
    license="BSD",
    zip_safe=False,
    keywords='django-shorturl',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=[
        'Django>=1.8,<1.9',
        'python-social-auth',
    ],
)
