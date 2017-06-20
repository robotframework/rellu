import pytest

from rellu.releasenotes import Version, PreviewMatcher


def test_version():
    for milestone in ('1.0', '1.6.2017'):
        version = Version(milestone)
        assert version.version == milestone
        assert version.milestone == milestone
        assert version.preview is None
        for preview in ('a1', 'b2', 'rc3', '.dev123'):
            version = Version(milestone + preview)
            assert version.version == milestone + preview
            assert version.milestone == milestone
            assert version.preview == preview


def test_invalid_version():
    for invalid in ('invalid', '1', '1.x', '1.0beta1', '1.0b'):
        with pytest.raises(ValueError):
            Version(invalid)


def test_preview_matcher():
    matcher = PreviewMatcher('a1')
    assert matcher.match('alpha 1')
    assert not matcher.match('alpha 2')
    assert not matcher.match('beta 1')
    assert not matcher.match('rc 2')

    matcher = PreviewMatcher('a2')
    assert matcher.match('alpha 1')
    assert matcher.match('alpha 2')
    assert not matcher.match('beta 1')
    assert not matcher.match('rc 2')

    matcher = PreviewMatcher('b2')
    assert matcher.match('alpha 1')
    assert matcher.match('alpha 2')
    assert matcher.match('beta 1')
    assert not matcher.match('rc 2')

    matcher = PreviewMatcher('rc2')
    assert matcher.match('alpha 1')
    assert matcher.match('alpha 2')
    assert matcher.match('beta 1')
    assert matcher.match('rc 2')


def test_invalid_preview():
    for invalid in (None, 'x1'):
        with pytest.raises(ValueError):
            PreviewMatcher(invalid)
