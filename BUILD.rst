Creating ``rellu`` releases
===========================

These instructions cover steps needed to create new releases of the ``rellu``
tool. Many individual steps are automated, but we don't want to automate
the whole procedure because it would be hard to react if something goes
terribly wrong. When applicable, the steps are listed as commands that can
be copied and executed on the command line.

.. contents::
   :depth: 1

Preconditions
-------------

Operating system and Python requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Generating releases has only been tested on Linux, but it ought to work the
same way also on OSX and other unixes. Generating releases on Windows may
work but is not tested, supported, or recommended.

Creating releases is only supported with Python 3.6 or newer. If you are
using Ubuntu or one of its derivatives and don't have Python 3.6 in the
official package repository, you may consider using the
`Dead Snakes PPA <https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa>`_.

The ``pip`` and ``invoke`` commands below are also expected to run on Python
3.6+. Alternatively, it's possible to use the ``python3.6 -m pip`` approach
to run these commands.

Required Python modules
~~~~~~~~~~~~~~~~~~~~~~~

Many steps are automated using `Invoke <http://pyinvoke.org>`_ and also
other tools/modules such as `twine <https://pypi.python.org/pypi/twine>`_
are needed. A pre-condition is installing all these tools, and that's easiest
done using `pip <http://pip-installer.org>`_ and the `<requirements-build.txt>`_
file::

    pip install -r requirements-build.txt

Using Invoke
~~~~~~~~~~~~

Invoke tasks are defined in `<tasks.py>`_ file and they are executed from
the command line like::

    inv[oke] task [options]

Run ``invoke`` without arguments for help. All tasks can be listed using
``invoke --list`` and each task's usage with ``invoke --help task``.

Different Git workflows
~~~~~~~~~~~~~~~~~~~~~~~

Git commands used below always expect that ``origin`` is the project main
repository. If that's not the case, and instead ``origin`` is your personal
fork, you probably still want to push to the main repository. In that case
you need to add ``upstream`` or similar to ``git push`` commands before
running them.

Preparation
-----------

1. Check that you are on the master branch and have nothing left to commit,
   pull, or push::

      git branch
      git status
      git pull --rebase
      git push

2. Clean up::

      invoke clean

3. Set version information to a shell variable to ease copy-pasting further
   commands. Add ``aN``, ``bN`` or ``rcN`` postfix if creating a pre-release::

      VERSION=<version>

   For example, ``VERSION=3.0.1`` or ``VERSION=3.1a2``.

Release notes
-------------

1. Generate a template for the release notes. Either first create shell
   variables with GitHub login info or just replace them in the command
   to actually generate the notes::

      GITHUB_USERNAME=<username>
      GITHUB_PASSWORD=<password>

      invoke release-notes -w -v $VERSION -u $GITHUB_USERNAME -p $GITHUB_PASSWORD

   The ``-v $VERSION`` option can be omitted if `version is already set
   <Set version_>`__. Omit the `-w` option if you just want to get release
   notes printed to the console, not written to a file.

   When generating release notes for a preview release like ``3.0.2rc1``,
   the list of issues is only going to contain issues with that label
   (e.g. ``rc1``) or with a label of an earlier preview release (e.g.
   ``alpha1``, ``beta2``).

2. Fill the missing details in the generated release notes template.

3. Make sure that issues have correct information:

   - All issues should have type (bug, enhancement or task) and priority set.
     Notice that issues with the task type are automatically excluded from
     the release notes.
   - Issue priorities should be consistent.
   - Issue titles should be informative. Consistency is good here too, but
     no need to overdo it.

   If information needs to be added or edited, its better to edit it in the
   issue tracker than in the generated release notes. This allows re-generating
   the list of issues later if more issues are added.

4. Add, commit and push::

      git add doc/rellu-$VERSION.rst
      git commit -m "Release notes for $VERSION" doc/rellu-$VERSION.rst
      git push

5. Update later if necessary. Writing release notes is typically the biggest
   task when generating releases, and getting everything done in one go is
   often impossible.

Set version
-----------

1. Set version information in `<rellu/__init__.py>`_::

      invoke set-version $VERSION

2. Commit and push changes::

      git commit -m "Updated version to $VERSION" rellu/__init__.py
      git push

Tagging
-------

1. Create an annotated tag and push it::

      git tag -a v$VERSION -m "Release $VERSION"
      git push --tags

2. Add short release notes to GitHub's `releases page
   <https://github.com/robotframework/rellu/releases>`_
   with a link to the full release notes.

Creating distributions
----------------------

1. Checkout the earlier created tag if necessary::

      git checkout v$VERSION

2. Cleanup. This removes temporary files as well as ``build`` and ``dist``
   directories::

      invoke clean

3. Create source distribution and `wheel <http://pythonwheels.com>`_::

      python3 setup.py sdist bdist_wheel
      ls -l dist

   Distributions can be tested locally if needed.

4. Upload to PyPI::

      twine upload dist/*

5. Verify that project page at `PyPI <https://pypi.python.org/pypi/rellu>`_
   looks good.

6. Test installation (add ``--pre`` with pre-releases)::

      pip install rellu --upgrade

Post actions
------------

1. Back to master if needed::

      git checkout master

2. Set dev version based on the previous version::

      invoke set-version dev
      git commit -m "Back to dev version" rellu/__init__.py
      git push

   For example, ``3.2.1`` is changed to ``3.2.2.dev`` with the current date
   appended.

3. Close the `issue tracker milestone
   <https://github.com/robotframework/rellu/milestones>`__.

Announcements
-------------

Probably no public announcements needed for this project.
