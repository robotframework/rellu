from pathlib import Path
import sys

from invoke import task

from rellu.tasks import clean
from rellu import initialize_labels, Version, ReleaseNotesGenerator


assert Path.cwd() == Path(__file__).parent

REPOSITORY = 'robotframework/rellu'
VERSION_PATH = Path('rellu/__init__.py')
RELEASE_NOTES_PATH = Path('doc/rellu-{version}.rst')
RELEASE_NOTES_TITLE = 'Rellu {version}'
RELEASE_NOTES_INTRO = '''
Rellu provides utilities to ease creating releases.
Rellu {version} is a new release with
**UPDATE** enhancements and bug fixes. **ADD more intro stuff...**

**REMOVE this section with final releases or if release notes contain
all issues otherwise.**
All issues targeted for Rellu {version.milestone} can be found from the
`issue tracker`_.

**REMOVE ``--pre`` from the next command with final releases.**
If you have pip_ installed, just run

::

   pip install --pre --upgrade rellu

to install the latest available release or use

::

   pip install rellu=={version}

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

Rellu {version} was released on {date}.

.. _Issue tracker: https://github.com/robotframework/rellu/issues?q=milestone%3A{version.milestone}
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/rellu
'''


@task
def set_version(ctx, version):
    """Set project version in ``rellu/__init__.py`` file.

    Args:
        version: Project version to set or ``dev`` to set development version.

    Following PEP-440 compatible version numbers are supported:
    - Final version like 3.0 or 3.1.2.
    - Alpha, beta or release candidate with an incremented number like
      3.0a1, 3.0b3 or 3.0.1rc1.
    - Development version with an incremented number like 3.0.dev1 or
      3.1a1.dev2.

    When the given version is ``dev``, the existing version number is updated
    to the next suitable development version. For example, 3.0 -> 3.0.1.dev1,
    3.1.1 -> 3.1.2.dev1, 3.2a1 -> 3.2a2.dev1, 3.2.dev1 -> 3.2.dev2.
    """
    version = Version(version, VERSION_PATH)
    version.write()
    print(version)


@task
def print_version(ctx):
    """Print the current project version."""
    print(Version(path=VERSION_PATH))


@task
def release_notes(ctx, version=None, username=None, password=None, write=False):
    """Generates release notes based on issues in the issue tracker.

    Args:
        version:  Generate release notes for this version. If not given,
                  generated them for the current version.
        username: GitHub username.
        password: GitHub password.
        write:    When set to True, write release notes to a file overwriting
                  possible existing file. Otherwise just print them to the
                  terminal.

    Username and password can also be specified using ``GITHUB_USERNAME`` and
    ``GITHUB_PASSWORD`` environment variable, respectively. If they aren't
    specified at all, communication with GitHub is anonymous and typically
    pretty slow.
    """
    version = Version(version, VERSION_PATH)
    file = RELEASE_NOTES_PATH if write else sys.stdout
    generator = ReleaseNotesGenerator(REPOSITORY, RELEASE_NOTES_TITLE,
                                      RELEASE_NOTES_INTRO)
    generator.generate(version, username, password, file)


@task
def initialize(ctx, username=None, password=None):
    """Initialize project by setting labels in the issue tracker.

    Args:
        username: GitHub username.
        password: GitHub password.

    Username and password can also be specified using ``GITHUB_USERNAME`` and
    ``GITHUB_PASSWORD`` environment variable, respectively.
    """
    initialize_labels(REPOSITORY, username, password)
