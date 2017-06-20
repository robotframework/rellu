import re
import sys
import time
from functools import total_ordering

from .utils import get_repository


class ReleaseNoteGenerator:
    pre_intro = '''
.. default-role:: code
'''
    post_intro = '''
.. contents::
   :depth: 2
   :local:
'''.strip()

    def __init__(self, repository, title, intro, default_targets=(),
                 stream=sys.stdout):
        self.repository = repository
        self.title = title
        self.intro = intro
        self.default_targets = default_targets
        self.stream = stream

    def generate(self, version, username=None, password=None):
        version = Version(version)
        issues = self._get_issues(version, username, password)
        self._write_intro(version)
        self._write_most_important_enhancements(issues, version)
        self._write_backwards_incompatible_changes(issues, version)
        self._write_deprecated_features(issues, version)
        self._write_acknowledgements(issues)
        self._write_issue_table(issues, version)
        self._write_targets(issues)

    def _get_issues(self, version, username=None, password=None):
        repository = get_repository(self.repository, username, password)
        issues = self._get_issues_in_milestone(repository, version)
        if version.preview:
            matcher = PreviewMatcher(version.preview)
            issues = (i for i in issues if matcher.match_any(i.labels))
        return sorted(issues)

    def _get_issues_in_milestone(self, repository, version):
        milestone = self._get_milestone(repository, version)
        for data in repository.get_issues(milestone=milestone, state='all'):
            issue = Issue(data, repository.name)
            if issue.include_in_release_notes:
                yield issue

    def _get_milestone(self, repository, version):
        for milestone in repository.get_milestones(state='all'):
            if milestone.title == version.milestone:
                return milestone
        raise ValueError(f"Milestone '{version.milestone}' not found from "
                         f"repository '{repository.name}'.")

    def _write_intro(self, version):
        self._write_header(self.title.format(version=version), level=1)
        intro = self.intro.format(version=version,
                                  date=time.strftime('%A %B %-d, %Y'))
        self._write(self.pre_intro, newlines=2)
        self._write(intro, newlines=2)
        self._write(self.post_intro)

    def _write_most_important_enhancements(self, issues, version):
        self._write_issues_with_label('Most important enhancements', issues,
                                      version, 'prio-critical', 'prio-high')

    def _write_backwards_incompatible_changes(self, issues, version):
        self._write_issues_with_label('Backwards incompatible changes', issues,
                                      version, 'bwic')

    def _write_deprecated_features(self, issues, version):
        self._write_issues_with_label('Deprecated features', issues, version,
                                      'depr')

    def _write_acknowledgements(self, issues):
        self._write_header('Acknowledgements')
        self._write('**UPDATE** based on AUTHORS.txt or similar.')

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
        self.stream.write(message)


class Version(object):
    match = re.compile(r'^(?P<milestone>\d+\.\d+(?:\.\d+)?)'
                       r'(?P<preview>(?:a|b|rc|.dev)\d+)?$').match

    def __init__(self, version):
        match = self.match(version)
        if not match:
            raise ValueError(f'Invalid version {version!r}.')
        self.version = version
        self.milestone = match.group('milestone')
        self.preview = match.group('preview')

    def __str__(self):
        return self.version


@total_ordering
class Issue(object):
    PRIORITIES = ['critical', 'high', 'medium', 'low', '']
    TYPES = ['bug', 'enhancement', 'task']

    def __init__(self, issue, repository):
        self.id = f'#{issue.number}'
        self.summary = issue.title
        self.labels = [label.name for label in issue.get_labels()]
        self.type = self._get_type()
        self.priority = self._get_priority()
        self.url = f'https://github.com/{repository}/issues/{issue.number}'

    def _get_type(self):
        return self._get_label(*self.TYPES)

    def _get_label(self, *values):
        for value in values:
            if value in self.labels:
                return value
        return ''

    def _get_priority(self):
        labels = ['prio-' + prio for prio in self.PRIORITIES if prio]
        priority = self._get_label(*labels)
        return priority.split('-')[1] if priority else ''

    @property
    def preview(self):
        for label in self.labels:
            if label.startswith(('alpha ', 'beta ', 'rc ')):
                return label
        return ''

    @property
    def include_in_release_notes(self):
        return self.type != 'task'

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


class PreviewMatcher:
    _preview_map = {
        'a1': 'alpha 1',
        'a2': 'alpha [12]',
        'a3': 'alpha [123]',
        'b1': r'(alpha \d|beta 1)',
        'b2': r'(alpha \d|beta [12])',
        'b3': r'(alpha \d|beta [123])',
        'rc1': r'(alpha \d|beta \d|rc 1)',
        'rc2': r'(alpha \d|beta \d|rc [12])',
        'rc3': r'(alpha \d|beta \d|rc [123])'
    }

    def __init__(self, preview):
        if preview not in self._preview_map:
            raise ValueError(f'Invalid preview {preview!r}.')
        pattern = self._preview_map[preview]
        self.match = re.compile(f'^{pattern}$').match

    def match_any(self, labels):
        return any(self.match(label) for label in labels)
