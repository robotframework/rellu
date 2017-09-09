from pathlib import Path
import sys

from invoke import task

from rellu.tasks import clean
from rellu import initialize_labels, Version
from rellu.releasenotes import ReleaseNotesGenerator


assert Path.cwd() == Path(__file__).parent

REPOSITORY = 'robotframework/rellu'
VERSION_PATH = Path('rellu/__init__.py')
RELEASE_NOTES_PATH = Path('doc/rellu-{version}.rst')
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
def set_version(ctx, version):
    version = Version(version, VERSION_PATH)
    version.write()
    print(version)


@task
def print_version(ctx):
    print(Version(path=VERSION_PATH))


@task
def initialize(ctx, username=None, password=None):
    initialize_labels(REPOSITORY, username, password)


@task
def release_notes(ctx, version=None, username=None, password=None, write=False):
    version = Version(version, VERSION_PATH)
    file = RELEASE_NOTES_PATH if write else sys.stdout
    generator = ReleaseNotesGenerator(REPOSITORY, RELEASE_NOTES_TITLE,
                                      RELEASE_NOTES_INTRO)
    generator.generate(version, username, password, file)
