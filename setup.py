#!/usr/bin/env python3.6

from os.path import abspath, dirname, join
import re

from setuptools import setup


NAME = 'rellu'
CLASSIFIERS = '''
Development Status :: 4 - Beta
License :: OSI Approved :: Apache Software License
Operating System :: OS Independent
Programming Language :: Python :: 3.6
Intended Audience :: Developers
Topic :: Software Development :: Build Tools
'''.strip().splitlines()
CURDIR = dirname(abspath(__file__))
with open(join(CURDIR, NAME, '__init__.py')) as source:
    VERSION = re.search("\n__version__ = '(.*)'\n", source.read()).group(1)
with open(join(CURDIR, 'README.rst')) as readme:
    README = readme.read()
with open(join(CURDIR, 'requirements.txt')) as requirements:
    REQUIREMENTS = requirements.read().splitlines()


setup(
    name             = NAME,
    version          = VERSION,
    packages         = [NAME],
    author           = 'Pekka Klärck and contributors',
    author_email     = 'robotframework@gmail.com',
    url              = 'https://github.com/robotframework/rellu',
    download_url     = 'https://pypi.python.org/pypi/rellu',
    license          = 'Apache License 2.0',
    description      = 'Tooling to ease creating releases',
    long_description = README,
    keywords         = 'releasing',
    platforms        = 'any',
    classifiers      = CLASSIFIERS,
    install_requires = REQUIREMENTS
)
