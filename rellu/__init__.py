"""Utilities to ease creating releases on GitHub.

These utilities are designed to be used by Robot Framework and tools/libraries
in its ecosystem, but they can be used by other projects too.

Utilities use Invoke <http://pyinvoke.org> internally. Project specific
BUILD.rst or similar ought to contain more details about releasing.

Requires Python >= 3.6 and invoke >= 0.20.
"""

import sys


__version__ = '0.2'


if sys.version_info < (3, 6):
    raise ImportError('Python 3.6 or newer required.')

try:
    from invoke import __version_info__ as invoke_version

    if invoke_version < (0, 20):
        raise ImportError
except ImportError:
    raise ImportError('invoke 0.20 or newer required.')


from .git import git_commit, git_push, git_tag
from .labels import initialize_labels
from .releasenotes import ReleaseNotesGenerator
from .version import get_version, set_version
from .utils import run
