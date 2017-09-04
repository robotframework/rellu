Creating ``rellu`` releases
===========================

These instructions cover steps needed to create new releases of the ``rellu``
tool. Most individual steps are automated, but we do not want to automate
the whole procedure because it would be hard to react if something goes
terribly wrong. When applicable, the steps are listed as commands that can
be copied and executed on the command line.

.. contents::

Preconditions
-------------

Most tasks are automated using `Invoke <http://pyinvoke.org>`_ tasks that
are defined in `<tasks.py>`_ file. A pre-condition is installing Invoke
and other tools used by tasks. This is easiest done using `pip
<http://pip-installer.org>`_ and the `<requirements.txt>`_ file::

    pip install -r requirements.txt

Invoke is executed from the command line like::

    inv[oke] task [options]

Run ``invoke`` without arguments for help. All tasks can be listed using
``invoke --list`` and each task's usage with ``invoke --help task``.

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

2. Fill the missing details in the template.

3. Add, commit and push::

      git add doc/rellu-$VERSION.rst
      git commit -m "Release notes for $VERSION" doc/rellu-$VERSION.rst
      git push

4. Add short release notes to GitHub's `releases page
   <https://github.com/robotframework/rellu/releases>`_
   with a link to the full release notes.

Set version
-----------

1. Set version information in `<rellu/__init__.py>`_::

      invoke set-version $VERSION

2. Commit and push changes::

      git commit -m "Updated version to $VERSION" rellu/__init__.py
      git push

Tagging
-------

Create an annotated tag and push it::

   git tag -a "v$VERSION" -m "Release $VERSION"
   git push --tags

Creating distributions
----------------------

1. Checkout the earlier created tag if necessary::

      git checkout v$VERSION

2. Cleanup. This removes temporary files as well as ``build`` and ``dist``
   directories::

      invoke clean

3. Create source distribution and wheel::

      python3 setup.py sdist bdist_wheel

   Test distributions locally if necessary.

4. Upload to PyPI::

      twine upload dist/*

5. Verify that https://pypi.python.org/pypi/rellu looks good.

6. Test installation (add ``--pre`` with pre-releases)::

      pip install rellu --upgrade

Post actions
------------

1. Set dev version based on the previous version. For example, ``3.2.1``
   is changed to ``3.2.2.dev`` with the current date appended.

      invoke set-version dev
      git commit -m "Back to dev version" rellu/__init__.py
      git push

2. Close `issue tracker milestone
   <https://github.com/robotframework/rellu/milestones>`__.

Announcements
-------------

Probably no public announcements needed for this project.
