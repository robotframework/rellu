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

from pathlib import Path

from .utils import run


def git_commit(paths, message, push=False, upstream=False, dry_run=False):
    if not isinstance(paths, (str, Path)):
        paths = ' '.join(str(p) for p in paths)
    run(f"git commit -m '{message}' {paths}", dry_run=dry_run)
    if push:
        git_push(upstream=upstream, dry_run=dry_run)


def git_push(tags=False, upstream=False, dry_run=False):
    command = 'git push' + ' --tags' if tags else ''
    run(command, dry_run=dry_run)
    if upstream:
        run(command + ' upstream', dry_run=dry_run)


def git_tag(version, upstream=False, dry_run=False):
    """Tag specified release.

    Creates an annotated tag and pushes changes.
    """
    run(f"git tag -a v{version} -m 'Release {version}'", dry_run=dry_run)
    git_push(tags=True, upstream=upstream, dry_run=dry_run)
