"""Utilities to ease creating releases on GitHub.

These utilities are designed to be used with Invoke <http://pyinvoke.org>.
Project specific BUILD.rst ought to contain more details about releasing.

These utilities are designed to be used by Robot Framework and tools/libraries
in its ecosystem, but they can be used by other projects too.

Requires Python 3 and invoke >= 0.13.
"""

import sys


__version__ = '0.0.2.dev20170526'


if sys.version_info < (3, 6):
    raise ImportError('Python 3.6 or newer required.')

try:
    from invoke import __version_info__ as invoke_version

    if invoke_version < (0, 13):
        raise ImportError
except ImportError:
    raise ImportError('invoke 0.13 or newer required.')
