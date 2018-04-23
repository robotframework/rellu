# Copyright 2017- Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Utilities to ease creating releases on GitHub.

These utilities are designed to be used by Robot Framework and tools/libraries
in its ecosystem, but they can be used by other projects too.

Utilities use Invoke <http://pyinvoke.org> internally. Project specific
BUILD.rst or similar ought to contain more details about releasing.

Requires Python >= 3.6 and invoke >= 0.20.
"""

import sys


__version__ = '0.7'


if sys.version_info < (3, 6):
    raise ImportError('Python 3.6 or newer required.')

try:
    from invoke import __version_info__ as invoke_version

    if invoke_version < (0, 20):
        raise ImportError
except ImportError:
    raise ImportError('invoke 0.20 or newer required.')


from .labels import initialize_labels
from .releasenotes import ReleaseNotesGenerator
from .version import Version
