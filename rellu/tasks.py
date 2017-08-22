import os
import shutil

from invoke import task, run

from .utils import announce_dists


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
def dist(ctx, upload=False, remove_dist=False):
    """Create source distribution.

    Args:
        upload:       Upload distribution to PyPI.
        remove_dist:  Control is 'dist' directory initially removed or not.
    """
    clean(ctx, remove_dist, create_dirs=True)
    run('python setup.py sdist' + (' upload' if upload else ''))
    announce_dists()
