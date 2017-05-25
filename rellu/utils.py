import os
import re
import time

from invoke import task, run


VERSION_PATTERN = "__version__ = '.*'"
VERSION_RE = re.compile('^(((?:\d+)\.\d+)(\.\d+)?)((a|b|rc|.dev)(\d+))?$')


def git_commit(paths, message, push=False):
    paths = ' '.join(str(p) for p in paths) if isinstance(paths, list) else paths
    run(f"git commit -m '{message}' {paths}")
    if push:
        run('git push')


def tag_release(version):
    """Tag specified release.

    Creates an annotated tag and pushes changes.
    """
    run(f"git tag -a {version} -m 'Release {version}'")
    run("git push --tags")


def announce_dists():
    print()
    print('Distributions:')
    for name in os.listdir('dist'):
        print(os.path.join('dist', name))


def set_version(version, path, pattern=VERSION_PATTERN):
    """Set version in the specified version file.

    TODO: Doc update

    Version can have these values:
    - Actual version number to use. See below for supported formats.
    - String 'dev' to update version to latest development version
      (e.g. 2.8 -> 2.8.1.dev, 2.8.1 -> 2.8.2.dev, 2.8a1 -> 2.8.dev) with
      the current date added or updated.
    - String 'keep' to keep using the previously set version.

    Given version must be in one of these PEP-440 compatible formats:
    - Stable version in 'X.Y' or 'X.Y.Z' format (e.g. 2.8, 2.8.6)
    - Pre-releases with 'aN', 'bN' or 'rcN' postfix (e.g. 2.8a1, 2.8.6rc2)
    - Development releases with '.devYYYYMMDD' postfix (e.g. 2.8.6.dev20141001)
      or with '.dev' alone (e.g. 2.8.6.dev) in which case date is added
      automatically.

    Args:
        version:  Version to use. See above for supported values and formats.
        push:     Commit and push changes to the remote repository.
    """
    if version != 'keep':
        if version == 'dev':
            version = _get_dev_version(path, pattern)
        version = _validate_version(version)
        write_version(version, path, pattern)
    else:
        version = read_version(path, pattern)
    return version


def _get_dev_version(path, pattern):
    previous = read_version(path, pattern)
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


def write_version(version, path, pattern=VERSION_PATTERN):
    replacement = pattern.replace('.*', version)
    with open(path) as file:
        content = re.sub(pattern, replacement, file.read())
    with open(path, 'w') as file:
        file.write(content)


def read_version(path, pattern=VERSION_PATTERN):
    pattern = pattern.replace('.*', '(.*)')
    with open(path) as file:
        content = file.read()
    match = re.search(pattern, content)
    return match.group(1)
