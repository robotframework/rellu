from pathlib import Path

from invoke import run


def git_commit(paths, message, push=False, upstream=False):
    if not isinstance(paths, (str, Path)):
        paths = ' '.join(str(p) for p in paths)
    run(f"git commit -m '{message}' {paths}")
    if push:
        git_push(upstream=upstream)


def git_push(tags=False, upstream=False):
    command = 'git push' + ' --tags' if tags else ''
    run(command)
    if upstream:
        run(command + ' upstream')


def tag_release(version, upstream=False):
    """Tag specified release.

    Creates an annotated tag and pushes changes.
    """
    run(f"git tag -a 'v{version}' -m 'Release {version}'")
    git_push(tags=True, upstream=upstream)
