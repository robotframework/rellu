from pathlib import Path
import sys

from invoke import task

from rellu.tasks import clean, dist
from rellu import git_commit, git_tag, get_version, initialize_labels, set_version
from rellu.releasenotes import ReleaseNotesGenerator


assert Path.cwd() == Path(__file__).parent

REPOSITORY = 'robotframework/rellu'
VERSION_FILE = Path('rellu/__init__.py')
RELEASE_NOTES_FILE = Path('doc/rellu-{version}.rst')
RELEASE_NOTES_TITLE = 'Rellu {version}'
RELEASE_NOTES_INTRO = '''
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
    print(f'Version set to {number}.')
    if push:
        git_commit(VERSION_FILE, f'Updated version to {number}', push=True)


@task
def print_version(ctx):
    print(get_version(VERSION_FILE))


@task
def initialize(ctx, username=None, password=None):
    initialize_labels(REPOSITORY, username, password)


@task
def release_notes(ctx, version=None, username=None, password=None, write=False):
    if not version:
        version = get_version(VERSION_FILE)
    file = RELEASE_NOTES_FILE if write else sys.stdout
    generator = ReleaseNotesGenerator(REPOSITORY, RELEASE_NOTES_TITLE,
                                      RELEASE_NOTES_INTRO)
    generator.generate(version, username, password, file)


@task
def tag_release(ctx, upstream=False, dry_run=False):
    version = get_version(VERSION_FILE)
    if version.dev:
        print(f'Cannot tag dev version {version}.')
    else:
        git_tag(version, upstream=upstream, dry_run=dry_run)
