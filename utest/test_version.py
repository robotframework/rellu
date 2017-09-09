import pytest

from invoke import Exit

from rellu.version import Version


def test_version():
    for milestone in ('1.0', '10.9.2017'):
        version = Version(milestone)
        assert version.version == milestone
        assert version.milestone == 'v' + milestone
        assert version.preview is None
        assert version.dev is None
        for preview in ('a1', 'b2', 'rc3'):
            version = Version(milestone + preview)
            assert version.version == milestone + preview
            assert version.milestone == 'v' + milestone
            assert version.preview == preview
            assert version.dev is None
        version = Version(milestone + '.dev1')
        assert version.version == milestone + '.dev1'
        assert version.milestone == 'v' + milestone
        assert version.preview is None
        assert version.dev == '.dev1'


def test_invalid_version():
    for invalid in ('invalid', '1', '1.x', '1.0beta1', '1.0b'):
        with pytest.raises(Exit):
            Version(invalid)


def test_is_included():
    for version, data in [('1.0a1', [('alpha 1', True),
                                     ('alpha 2', False),
                                     ('beta 1', False),
                                     ('rc 2', False)]),
                          ('1.0a2', [('alpha 1', True),
                                     ('alpha 2', True),
                                     ('beta 1', False),
                                     ('rc 2', False)]),
                          ('1.0b2', [('alpha 1', True),
                                     ('alpha 2', True),
                                     ('beta 1', True),
                                     ('rc 2', False)]),
                          ('1.0rc2', [('alpha 1', True),
                                      ('alpha 2', True),
                                      ('beta 1', True),
                                      ('rc 2', True)]),
                          ('1.0', [('alpha 1', True),
                                   ('alpha 2', True),
                                   ('beta 1', True),
                                   ('rc 2', True)])]:
        is_included = Version(version).is_included
        for preview, expected in data:
            assert is_included(IssueStub('v1.0', preview)) is expected
        assert is_included(IssueStub('v1.0', None)) is (version == '1.0')


class IssueStub:
    
    def __init__(self, milestone, preview):
        self.milestone = milestone
        self.preview = preview
