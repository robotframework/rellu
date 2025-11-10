===========
Rellu 0.8.0
===========


.. default-role:: code


Rellu provides utilities to ease creating releases.
Rellu 0.8.0 is a new release with enhancements to support
GitHub issue type and making issue order configurable.
This release also contains bug fix to correctly handle
regular expressions with escape sequences.

All issues targeted for Rellu v0.8.0 can be found from the
`issue tracker`_.

If you have pip_ installed, just run

::

   pip install --upgrade rellu

to install the latest available release or use

::

   pip install rellu==0.8.0

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

Rellu 0.8.0 was released on Monday November 10, 2025.

.. _Issue tracker: https://github.com/robotframework/rellu/issues?q=milestone%3Av0.8.0
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/rellu


.. contents::
   :depth: 2
   :local:

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#18`_
      - bug
      - medium
      - The use of rellu in the `robotframework-browser` project causes a SyntaxWarning: invalid escape sequence '\s'   tokens = re.split('\s{2,}', line)

Altogether 1 issue. View on the `issue tracker <https://github.com/robotframework/rellu/issues?q=milestone%3Av0.8.0>`__.

.. _#18: https://github.com/robotframework/rellu/issues/18
