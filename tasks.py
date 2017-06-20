from pathlib import Path

from rellu.tasks import clean
from rellu.utils import (git_commit, initialize_labels, set_version,
                         read_version, task)
from rellu.releasenotes import ReleaseNoteGenerator


assert Path.cwd() == Path(__file__).parent

VERSION_FILE = Path('rellu/__init__.py')
REPOSITORY = 'robotframework/rellu'
RELASE_NOTES_TITLE = 'Rellu {version}'
RELASE_NOTES_INTRO = '''
Rellu {version} is a new release with **UPDATE** enhancements and bug
fixes. **MORE intro stuff...**

**REMOVE reference to tracker if release notes contain all issues.**
All issues targeted for Rellu {version.milestone} can be found from the `issue tracker
<https://github.com/robotframework/rellu/issues?q=milestone%3A{version.milestone}>`_.

**ADD --pre with preview releases.**
If you have `pip <http://pip-installer.org>`_ installed, just run
`pip install --upgrade rellu` to install the latest release or use
`pip install rellu=={version}` to install exactly this version.
Alternatively you can download the source distribution from
`PyPI <https://pypi.python.org/pypi/rellu>`_ and install it manually.

Rellu {version} was released on {date}.
'''


@task
def version(ctx, number, push=False):
    number = set_version(number, path=VERSION_FILE)
    print(f'Version set to {number!r}.')
    if push:
        git_commit(VERSION_FILE, f'Updated version to {number}', push=True)


@task
def print_version(ctx):
    number = read_version(VERSION_FILE)
    print(f'Current version is {number!r}.')


@task
def initialize(ctx, username=None, password=None):
    initialize_labels(REPOSITORY, username, password)


@task
def release_notes(ctx, version=None, username=None, password=None):
    generator = ReleaseNoteGenerator(REPOSITORY, RELASE_NOTES_TITLE,
                                     RELASE_NOTES_INTRO)
    if not version:
        version = read_version(VERSION_FILE)
    generator.generate(version, username, password)
