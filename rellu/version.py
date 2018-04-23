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

import re

from invoke import Exit


VERSION_PATTERN = "__version__ = '(.*)'"


class Version(object):
    """Class representing versions in PEP-440 compatible format."""
    match = re.compile(r'^(?P<release>\d+\.\d+(\.\d+)?)'
                       r'(?P<pre>(a|b|rc)[12345])?'
                       r'(?P<dev>.dev\d+)?$').match
    preview_map = {
        'a1':  r'alpha 1',
        'a2':  r'alpha [12]',
        'a3':  r'alpha [123]',
        'a4':  r'alpha [1234]',
        'a5':  r'alpha [12345]',
        'b1':  r'(alpha [12345]|beta 1)',
        'b2':  r'(alpha [12345]|beta [12])',
        'b3':  r'(alpha [12345]|beta [123])',
        'b4':  r'(alpha [12345]|beta [1234])',
        'b5':  r'(alpha [12345]|beta [12345])',
        'rc1': r'(alpha [12345]|beta [12345]|rc 1)',
        'rc2': r'(alpha [12345]|beta [12345]|rc [12])',
        'rc3': r'(alpha [12345]|beta [12345]|rc [123])',
        'rc4': r'(alpha [12345]|beta [12345]|rc [1234])',
        'rc5': r'(alpha [12345]|beta [12345]|rc [12345])'
    }

    def __init__(self, version=None, path=None, pattern=VERSION_PATTERN):
        """Initialize based on given version of by version read from file.

        :param version: Version to use. If not given, version is read from file.
        :param path: File were version if read if not explicitly given.
            Also used by :meth:`write`.
        :param pattern: Pattern to use when reading/writing version information.

        Version can have these values:
        - No value. Version is read from file.
        - Actual version number to use. See below for supported formats.
        - String 'dev' to read the version from file and to update it to
          latest suitable development version (e.g. 3.0 -> 3.0.1.dev1,
          3.1.1 -> 3.1.2.dev1, 3.2a1 -> 3.2a2.dev1, 3.2.dev1 -> 3.2.dev2).

        Given version number must be in one of these PEP-440 compatible formats:
        - Stable version in 'X.Y' or 'X.Y.Z' format (e.g. 3.0, 3.2.1)
        - Pre-releases with 'aN', 'bN' or 'rcN' postfix (e.g. 3.0a1, 3.1.1rc2)
        - Development releases with '.devN' postfix (e.g. 3.2.1.dev1 or
          3.2a1.dev2).
        """
        if not version:
            version = Version.from_file(path, pattern).version
        elif version == 'dev':
            version = Version.from_file(path, pattern).to_dev().version
        match = self.match(version)
        if not match:
            raise Exit(f'Invalid version {version!r}.')
        self.release = match.group('release')
        self.preview = match.group('pre')
        self.dev = match.group('dev')
        self.path = path
        self.pattern = pattern

    @property
    def version(self):
        return self.release + (self.preview or '') + (self.dev or '')

    @property
    def milestone(self):
        return 'v' + self.release

    @classmethod
    def from_file(cls, path, pattern=VERSION_PATTERN):
        with open(path) as file:
            content = file.read()
        match = re.search(pattern, content)
        return Version(match.group(1), path, pattern)

    def to_dev(self):
        if self.dev:
            self._increment_dev()
        else:
            if self.preview:
                self._increment_preview()
            else:
                self._increment_release()
            self.dev = '.dev1'
        return self

    def _increment_dev(self):
        self.dev = '.dev' + str(int(self.dev[4:]) + 1)

    def _increment_preview(self):
        self.preview = self.preview[:-1] + str(int(self.preview[-1]) + 1)

    def _increment_release(self):
        tokens = self.release.split('.')
        if len(tokens) == 2:
            tokens.append('1')
        else:
            tokens[2] = str(int(tokens[2]) + 1)
        self.release = '.'.join(tokens)

    def is_included(self, issue):
        if issue.milestone != self.milestone:
            return False
        if not self.preview:
            return True
        if not issue.preview:
            return False
        pattern = self.preview_map[self.preview]
        return bool(re.match(f'^{pattern}$', issue.preview))

    def write(self):
        replacement = self.pattern.replace('(.*)', self.version)
        with open(self.path) as file:
            content = re.sub(self.pattern, replacement, file.read())
        with open(self.path, 'w') as file:
            file.write(content)

    def __str__(self):
        return self.version
