import re
import time


VERSION_PATTERN = "__version__ = '(.*)'"
VERSION_RE = re.compile('^(((?:\d+)\.\d+)(\.\d+)?)((a|b|rc|.dev)(\d+))?$')


def get_version(version_file, pattern=VERSION_PATTERN):
    with open(version_file) as file:
        content = file.read()
    match = re.search(pattern, content)
    return match.group(1)


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
        version = _get_dev_version(path, pattern)
    version = _validate_version(version)
    _write_version(version, path, pattern)
    return version


def _get_dev_version(path, pattern):
    previous = get_version(path, pattern)
    major, minor, pre = VERSION_RE.match(previous).groups()[1:4]
    if not pre:
        minor = '.{}'.format(int(minor[1:]) + 1 if minor else 1)
    if not minor:
        minor = ''
    return f'{major}{minor}.dev'


def _validate_version(version):
    if version.endswith('.dev'):
        version += time.strftime('%Y%m%d')
    if not VERSION_RE.match(version):
        raise ValueError("Invalid version '{}'.".format(version))
    return version


def _write_version(version, path, pattern):
    replacement = pattern.replace('(.*)', version)
    with open(path) as file:
        content = re.sub(pattern, replacement, file.read())
    with open(path, 'w') as file:
        file.write(content)


class Version(object):
    match = re.compile(r'^(?P<milestone>\d+\.\d+(?:\.\d+)?)'
                       r'(?P<preview>(?:a|b|rc)[123])?$').match
    preview_map = {
        'a1': 'alpha 1',
        'a2': 'alpha [12]',
        'a3': 'alpha [123]',
        'b1': r'(alpha \d|beta 1)',
        'b2': r'(alpha \d|beta [12])',
        'b3': r'(alpha \d|beta [123])',
        'rc1': r'(alpha \d|beta \d|rc 1)',
        'rc2': r'(alpha \d|beta \d|rc [12])',
        'rc3': r'(alpha \d|beta \d|rc [123])'
    }

    def __init__(self, version):
        match = self.match(version)
        if not match:
            raise ValueError(f'Invalid version for release notes {version!r}.')
        self.version = version
        self.milestone = 'v' + match.group('milestone')
        self.preview = match.group('preview')

    def is_included(self, issue):
        if not self.preview:
            return True
        pattern = self.preview_map[self.preview]
        match = re.compile(f'^{pattern}$').match
        return any(match(label) for label in issue.labels)

    def __str__(self):
        return self.version
