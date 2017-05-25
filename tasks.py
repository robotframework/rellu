from pathlib import Path

from rellu.tasks import clean
from rellu.utils import git_commit, set_version, read_version, task


assert Path.cwd() == Path(__file__).parent

VERSION_FILE = Path('rellu/__init__.py')


@task
def version(ctx, number, push=False):
    number = set_version(number, path=VERSION_FILE)
    print(f"Version set to '{number}'.")
    if push:
        git_commit(VERSION_FILE, f'Updated version to {number}', push=True)


@task
def print_version(ctx):
    number = read_version(VERSION_FILE)
    print(f"Current version is '{number}'.")
