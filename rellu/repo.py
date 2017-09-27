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

from github import Github
from invoke import Exit


def get_repository(name, username=None, password=None, auth_required=False):
    username = username or os.getenv('GITHUB_USERNAME')
    password = password or os.getenv('GITHUB_PASSWORD')
    if auth_required and not (username and password):
        raise Exit('Mandatory GitHub username/password not given.')
    return Github(username, password).get_repo(name)
