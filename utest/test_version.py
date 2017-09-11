import pytest

from invoke import Exit

from rellu.version import Version


def test_version():
    for milestone in ('1.0', '10.9.2017'):
        for preview in (None, 'a1', 'b2', 'rc3'):
            version = milestone + (preview or '')
            v = Version(version)
            assert v.version == version
            assert v.milestone == 'v' + milestone
            assert v.preview == preview
            assert v.dev is None
            v = Version(version + '.dev1')
            assert v.version == version + '.dev1'
            assert v.milestone == 'v' + milestone
            assert v.preview == preview
            assert v.dev == '.dev1'


def test_invalid_version():
    for invalid in ('invalid', '1', '1.x', '1.0beta1', '1.0b'):
        with pytest.raises(Exit):
            Version(invalid)


def test_to_dev():
    v = Version('1.0').to_dev('1')
    assert v.version == '1.0.1.dev1'
    assert v.milestone == 'v1.0.1'
    assert v.preview is None
    assert v.dev == '.dev1'
    v = Version('1.0a1').to_dev('2')
    assert v.version == '1.0a2.dev2'
    assert v.milestone == 'v1.0'
    assert v.preview == 'a2'
    assert v.dev == '.dev2'
    v = Version('1.0a1.dev1').to_dev('2')
    assert v.version == '1.0a1.dev2'
    assert v.milestone == 'v1.0'
    assert v.preview == 'a1'
    assert v.dev == '.dev2'


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
