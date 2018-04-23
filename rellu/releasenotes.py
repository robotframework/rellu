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
import sys
import time
from contextlib import contextmanager
from functools import total_ordering
from pathlib import Path

from invoke import Exit

from .repo import get_repository


class ReleaseNotesGenerator:
    pre_intro = '''
.. default-role:: code
'''
    post_intro = '''
.. contents::
   :depth: 2
   :local:
'''.strip()

    def __init__(self, repository, title, intro, default_targets=()):
        self.repository = repository
        self.title = title
        self.intro = intro
        self.default_targets = default_targets
        self._output = None

    def generate(self, version, username=None, password=None, file=sys.stdout):
        if version.dev:
            raise Exit(f'Cannot create release notes for development '
                       f"version '{version}'.")
        issues = self._get_issues(version, username, password)
        with self._output_enabled(file, version):
            self._write_intro(version)
            self._write_most_important_enhancements(issues, version)
            self._write_backwards_incompatible_changes(issues, version)
            self._write_deprecated_features(issues, version)
            self._write_acknowledgements(issues, version)
            self._write_issue_table(issues, version)
            self._write_targets(issues)

    def _get_issues(self, version, username=None, password=None):
        repository = get_repository(self.repository, username, password)
        issues = self._get_issues_in_milestone(repository, version)
        return sorted(issues)

    def _get_issues_in_milestone(self, repository, version):
        milestone = self._get_milestone(repository, version)
        for data in repository.get_issues(milestone=milestone, state='all'):
            issue = Issue(data, repository.full_name)
            if issue.included_in_release_notes(version):
                yield issue

    def _get_milestone(self, repository, version):
        for milestone in repository.get_milestones(state='all'):
            if milestone.title == version.milestone:
                return milestone
        raise Exit(f"Milestone '{version.milestone}' not found from "
                   f"repository '{repository.full_name}'.")

    @contextmanager
    def _output_enabled(self, file, version):
        if isinstance(file, (str, Path)):
            self._output = open(str(file).format(version=version), 'w')
            close = True
        else:
            self._output = file
            close = False
        try:
            yield
        finally:
            if close:
                print(self._output.name)
                self._output.close()
            self._output = None

    def _write_intro(self, version):
        self._write_header(self.title.format(version=version), level=1)
        intro = self.intro.format(version=version,
                                  date=time.strftime('%A %B %-d, %Y'))
        self._write(self.pre_intro)
        self._write(intro, newlines=2)
        self._write(self.post_intro)

    def _write_most_important_enhancements(self, issues, version):
        self._write_issues_with_label('Most important enhancements',
                                      issues, version,
                                      'priority: critical', 'priority: high')

    def _write_backwards_incompatible_changes(self, issues, version):
        self._write_issues_with_label('Backwards incompatible changes',
                                      issues, version,
                                      'backwards incompatible')

    def _write_deprecated_features(self, issues, version):
        self._write_issues_with_label('Deprecated features',
                                      issues, version,
                                      'deprecation')

    def _write_acknowledgements(self, issues, version):
        self._write_issues_with_label('Acknowledgements',
                                      issues, version,
                                      'acknowledge')

    def _write_issue_table(self, issues, version):
        self._write_header('Full list of fixes and enhancements')
        self._write('''
.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
'''.strip())
        prefix1 = '    * - '
        prefix2 = '      - '
        if version.preview:
            self._write('      - Added')
        for issue in issues:
            self._write(prefix1 + issue.id)
            self._write(prefix2 + issue.type)
            self._write(prefix2 + issue.priority)
            self._write(prefix2 + issue.summary)
            if version.preview:
                self._write(prefix2 + issue.preview.replace(' ', u'\xa0'))
        self._write()
        self._write('Altogether {} issue{}. View on the `issue tracker '
                    '<https://github.com/{}/issues?q=milestone%3A{}>`__.'
                    .format(len(issues), 's' if len(issues) != 1 else '',
                            self.repository, version.milestone))

    def _write_targets(self, issues):
        self._write()
        for target in self.default_targets:
            self._write(target)
        for issue in issues:
            self._write(f'.. _{issue.id}: {issue.url}', link_issues=False)

    def _write_header(self, header, level=2):
        if level > 1:
            self._write()
        underline = {1: '=', 2: '=', 3: '-', 4: '~'}[level] * len(header)
        if level == 1:
            self._write(underline)
        self._write(header)
        self._write(underline, newlines=2)

    def _write_issues_with_label(self, header, issues, version, *labels):
        issues = [issue for issue in issues
                  if any(label in issue.labels for label in labels)]
        if not issues:
            return
        self._write_header(header)
        self._write('**EXPLAIN** or remove these.', newlines=2)
        for issue in issues:
            self._write(f'- {issue.summary} ({issue.id}', newlines=0)
            if version.preview and issue.preview:
                self._write(f', {issue.preview})')
            else:
                self._write(')')

    def _write(self, message='', newlines=1, link_issues=True):
        message += '\n' * newlines
        if link_issues:
            message = re.sub(r'(#\d+)', r'`\1`_', message)
        self._output.write(message)


@total_ordering
class Issue(object):
    NOT_SET = '---'
    PRIORITIES = ['critical', 'high', 'medium', 'low', NOT_SET]
    TYPES = ['bug', 'enhancement', 'task', NOT_SET]

    def __init__(self, issue, repository):
        self.id = f'#{issue.number}'
        self.milestone = issue.milestone.title
        self.summary = issue.title
        self.labels = [label.name for label in issue.get_labels()]
        self.url = f'https://github.com/{repository}/issues/{issue.number}'

    @property
    def preview(self):
        for label in self.labels:
            if label.startswith(('alpha ', 'beta ', 'rc ')):
                return label
        return None

    @property
    def type(self):
        for label in self.labels:
            if label in self.TYPES:
                return label
        return self.NOT_SET

    @property
    def priority(self):
        priorities = ['priority: ' + prio for prio in self.PRIORITIES]
        for label in self.labels:
            if label in priorities:
                return label.split(': ')[1]
        return self.NOT_SET

    def included_in_release_notes(self, version):
        if self.type == 'task':
            return False
        return version.is_included(self)

    @property
    def sort_key(self):
        return (self.PRIORITIES.index(self.priority),
                self.TYPES.index(self.type),
                self.id)

    def __eq__(self, other):
        return isinstance(other, Issue) and self.id == other.id

    def __lt__(self, other):
        return self.sort_key < other.sort_key

    def __str__(self):
        return f'{self.id} {self.summary}'
