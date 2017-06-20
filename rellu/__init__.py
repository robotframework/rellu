"""Utilities to ease creating releases on GitHub.

These utilities are designed to be used by Robot Framework and tools/libraries
in its ecosystem, but they can be used by other projects too.

Utilities use Invoke <http://pyinvoke.org> internally. Project specific
BUILD.rst or similar ought to contain more details about releasing.

Requires Python >= 3.6 and invoke >= 0.13.
"""

import sys


__version__ = '0.1.dev20170620'


if sys.version_info < (3, 6):
    raise ImportError('Python 3.6 or newer required.')

try:
    from invoke import __version_info__ as invoke_version

    if invoke_version < (0, 13):
        raise ImportError
except ImportError:
    raise ImportError('invoke 0.13 or newer required.')
