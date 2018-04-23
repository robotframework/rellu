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

from .repo import get_repository


LABELS = '''
bug                 d73a4a    Something isn't working
enhancement         a2eeef    Proposal for a new feature or enhancement
task                ededed    Generic task not listed in release notes

alpha 1             ffffff
alpha 2             ffffff
alpha 3             ffffff
beta 1              ffffff
beta 2              ffffff
beta 3              ffffff
rc 1                ffffff
rc 2                ffffff
rc 3                ffffff

bwic                fbca04    Backwards-incompatible change
depr                fef2c0    Deprecated feature

duplicate           000000    This issue or pull request already exists
wont fix            000000    This will not be worked on
invalid             000000    This doesn't seem right
in progress         ededed    Development started
pending             ededed    Development stalled
needs review        ededed    Review needed

good first issue    7057ff    Good for newcomers
help wanted         008672    Extra help appreciated
acknowledge         bc82e0    Contribution to be acknowledged in release notes

prio-critical       00441b
prio-high           006d2c
prio-medium         238b45
prio-low            41ae76
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
    name = line[:20].strip()
    color = line[20:30].strip()
    description = line[30:].strip()
    return name, color, description


def _normalize(label):
    return label.lower().replace(' ', '')
