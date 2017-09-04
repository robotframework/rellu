import re
import time


VERSION_PATTERN = "__version__ = '(.*)'"


def get_version(version_file, pattern=VERSION_PATTERN):
    return Version.from_file(version_file, pattern)


def set_version(version, path, pattern=VERSION_PATTERN):
    """Set version in the specified version file.

    TODO: Doc update

    Version can have these values:
    - Actual version number to use. See below for supported formats.
    - String 'dev' to update version to latest development version
      (e.g. 2.8 -> 2.8.1.dev, 2.8.1 -> 2.8.2.dev, 2.8a1 -> 2.8.dev) with
      the current date added or updated.

    Given version must be in one of these PEP-440 compatible formats:
    - Stable version in 'X.Y' or 'X.Y.Z' format (e.g. 2.8, 2.8.6)
    - Pre-releases with 'aN', 'bN' or 'rcN' postfix (e.g. 2.8a1, 2.8.6rc2)
    - Development releases with '.devYYYYMMDD' postfix (e.g. 2.8.6.dev20141001)
      or with '.dev' alone (e.g. 2.8.6.dev) in which case date is added
      automatically.

    Args:
        version:  Version to use. See above for supported values and formats.
        path:     Path to the file containing version information.
        pattern:  Pattern specifying how version is set.
    """
    if version == 'dev':
        version = Version.from_file(path, pattern).get_dev_version()
    else:
        version = Version(version)
    version.write(path, pattern)
    return version


class Version(object):
    """Class representing versions in PEP-440 compatible format."""
    match = re.compile(r'^(?P<number>\d+\.\d+(\.\d+)?)'
                       r'((?P<pre>(a|b|rc)[12345])|(?P<dev>.dev\d+))?$').match
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

    def __init__(self, version):
        if version.endswith('.dev'):
            version += time.strftime('%Y%m%d')
        match = self.match(version)
        if not match:
            raise ValueError(f'Invalid version {version!r}.')
        self.version = version
        self.milestone = 'v' + match.group('number')
        self.preview = match.group('pre')
        self.dev = match.group('dev')

    @classmethod
    def from_file(cls, version_file, pattern=VERSION_PATTERN):
        with open(version_file) as file:
            content = file.read()
        match = re.search(pattern, content)
        return Version(match.group(1))

    def is_included(self, issue):
        if issue.milestone != self.milestone:
            return False
        if not self.preview:
            return True
        pattern = self.preview_map[self.preview]
        return bool(re.match(f'^{pattern}$', issue.preview))

    def get_dev_version(self):
        number = self.milestone[1:]
        if not self.dev:
            number = self._bump_version(number)
        return Version(number + '.dev')

    def _bump_version(self, number):
        tokens = number.split('.')
        if len(tokens) == 2:
            tokens.append('1')
        else:
            tokens[2] = str(int(tokens[2]) + 1)
        return '.'.join(tokens)

    def write(self, path, pattern=VERSION_PATTERN):
        replacement = pattern.replace('(.*)', self.version)
        with open(path) as file:
            content = re.sub(pattern, replacement, file.read())
        with open(path, 'w') as file:
            file.write(content)

    def __str__(self):
        return self.version
