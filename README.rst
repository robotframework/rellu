rellu -- Utilities to ease creating releases
============================================

This project contains tooling and templates to ease creating releases
on GitHub_ and publishing them on PyPI_. Designed to be used by
`Robot Framework`_ and tools and libraries in its ecosystem, but can
naturally be used also by other projects.

To be able to take this project into use, you should know at least
basics of `Python packaging`_.

Main features
-------------

- Utilities that can be used by custom Invoke_ tasks. These utilities
  are importable directly from the `rellu module`_:

  - Setting project version, including automatically setting it to
    the next suitable development version.
  - Setting common labels in the issue tracker.
  - Generating release notes based on issues in the tracker. Requires
    project to use pre-defined labels.

- Generic Invoke_ tasks in the `rellu.tasks module`_:

  - Cleaning temporary files and directories.

- `tasks.py`_ file implementing Invoke_ tasks using the aforementioned
  utilities. Other projects can use it as an example or template.

- Step-by-step instructions for creating releases in `BUILD.rst`_ file
  using Invoke_ tasks defined in the `tasks.py`_ file, git, and other tools.
  Also this file can be used as a template.

- `setup.py`_ using general good practices that can also be used as
  a template. There's also super simple `MANIFEST.in`_, but this project
  doesn't need ``setup.cfg``.

Dependencies
------------

Rellu is designed to be used together with Invoke_ which is also used
internally. All project dependencies are listed in the `requirements.txt`_
and `requirements-build.txt`_ files.

Rellu itself works only with Python 3.6 or never, but projects it is used
with can naturally support also older Python releases. Rellu is developed and
tested on Linux, but ought to work just fine also on OSX. Using it on
Windows may work, but that's not tested or supported.

Required project setup
----------------------

To be able to generate release notes automatically, issue trackers must
be configured using these rules:

- Milestones must match project versions and use format ``v1.2`` or ``v1.2.1``.

- Labels must be configured using the provided utility.

- Milestones and labels must be used consistently:

  - Valid issues must have type defined as a label ``bug``, ``enhancement``
    or ``task``. Issues with the task type are not included in release notes.
  - Issues should have priority set. See various ``prio-`` labels.
  - Issues belonging to a certain milestone should have that milestone set.
  - Issues included into a certain preview releases should have a matching
    label set (e.g. ``a1``, ``b2``, ``rc3``).


.. _GitHub: https://github.com
.. _PyPI: http://pypi.python.org
.. _Invoke: http://pyinvoke.org
.. _Robot Framework: http://robotframework.org
.. _Python packaging: https://packaging.python.org
.. _rellu module: https://github.com/robotframework/rellu/blob/master/rellu/__init__.py
.. _rellu.tasks module: https://github.com/robotframework/rellu/blob/master/rellu/tasks.py
.. _tasks.py: https://github.com/robotframework/rellu/blob/master/tasks.py
.. _BUILD.rst: https://github.com/robotframework/rellu/blob/master/BUILD.rst
.. _setup.py: https://github.com/robotframework/rellu/blob/master/setup.py
.. _MANIFEST.in: https://github.com/robotframework/rellu/blob/master/MANIFEST.in
.. _requirements.txt: https://github.com/robotframework/rellu/blob/master/requirements.txt
.. _requirements-build.txt: https://github.com/robotframework/rellu/blob/master/requirements-build.txt
