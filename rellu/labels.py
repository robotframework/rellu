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

import re

from invoke import Exit

from .repo import get_repository


LABELS = '''
bug                       d73a4a
enhancement               a2eeef
task                      ededed    Generic task not listed in release notes

alpha 1                   ffffff
alpha 2                   ffffff
alpha 3                   ffffff
beta 1                    ffffff
beta 2                    ffffff
beta 3                    ffffff
rc 1                      ffffff
rc 2                      ffffff
rc 3                      ffffff

backwards incompatible    fbca04
deprecation               fef2c0

duplicate                 000000
wont fix                  000000
invalid                   000000
in progress               ededed
pending                   ededed
needs review              ededed

good first issue          7057ff    Good for newcomers
help wanted               008672    Extra help appreciated
acknowledge               bc82e0    To be acknowledged in release notes

priority: critical        00441b
priority: high            006d2c
priority: medium          238b45
priority: low             41ae76
'''


def initialize_labels(repository, username=None, password=None):
    repository = get_repository(repository, username, password,
                                auth_required=True)
    labels = [_parse_label(line)
              for line in LABELS.splitlines() if line.strip()]
    existing_labels = {_normalize(label.name): label.name
                       for label in repository.get_labels()}
    for name, color, description in labels:
        try:
            normalized = existing_labels[_normalize(name)]
        except KeyError:
            repository.create_label(name, color, description)
        else:
            repository.get_label(normalized).edit(name, color, description)


def _parse_label(line):
    tokens = re.split('\s{2,}', line)
    if len(tokens) == 2:
        tokens.append('')
    if len(tokens) != 3 or len(tokens[1]) != 6:
        raise Exit(f'Invalid label information:\n{line}')
    return tokens


def _normalize(label):
    return label.lower().replace(' ', '')
