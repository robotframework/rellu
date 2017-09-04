# Copyright 2017- Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import shutil
import sys
from pathlib import Path

from invoke import task

from .run import run


@task
def clean(ctx, remove_dist=True, create_dirs=False):
    """Clean the workspace.

    By default deletes 'build' and 'dist' directories and removes '*.pyc',
    '*$py.class' and '*~' files.

    Args:
        remove_dist:  Remove also 'dist' (default).
        create_dirs:  Re-create 'build' and 'dist' after removing them.
    """
    for name in ['build', 'dist']:
        if os.path.isdir(name) and (name != 'dist' or remove_dist):
            print(f'Removing directory {name!r}.')
            shutil.rmtree(name)
        if create_dirs and not os.path.isdir(name):
            print(f'Creating directory {name!r}.')
            os.mkdir(name)
    print('Removing temporary files.')
    for directory, dirs, files in os.walk('.'):
        for name in files:
            if name.endswith(('.pyc', '$py.class', '~')):
                os.remove(os.path.join(directory, name))
        if '__pycache__' in dirs:
            shutil.rmtree(os.path.join(directory, '__pycache__'))


@task
def dist(ctx, wheel=True, universal=True, upload=False, remove_dist=True,
         dry_run=False):
    """Create source distribution.

    Args:
        upload:       Upload distribution to PyPI.
        remove_dist:  Control is 'dist' directory initially removed or not.
        dry_run:      Just print commands to execute, don't run them.
    """
    clean(ctx, remove_dist, create_dirs=True)
    command = f'{sys.executable} setup.py sdist'
    if wheel:
        command += ' bdist_wheel'
        if universal:
            command += ' --universal'
    run(command, dry_run=dry_run)
    if upload:
        run(f'{sys.executable} -m twine upload dist/*', dry_run=dry_run)
    _announce_dists()


def _announce_dists():
    print()
    print('Distributions:')
    for path in Path('dist').iterdir():
        print(path)
