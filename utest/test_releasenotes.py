import io
from types import SimpleNamespace

import pytest
from invoke import Exit

from rellu import releasenotes
from rellu.releasenotes import Issue, ReleaseNotesGenerator
from rellu.version import Version


def github_issue(number=1, labels=(), fields=()):
    field_values = [
        {
            "issue_field_name": name,
            "data_type": "single_select",
            "value": value,
            "single_select_option": {"name": value},
        }
        for name, value in fields
    ]
    return SimpleNamespace(
        number=number,
        milestone=SimpleNamespace(title="v1.0"),
        title=f"Issue {number}",
        type=None,
        get_labels=lambda: [SimpleNamespace(name=label) for label in labels],
        _rawData={"number": number, "issue_field_values": field_values},
    )


def test_priority_from_priority_field():
    issue = Issue(github_issue(fields=[("Priority", "High")]), "org/repo")
    assert issue.priority == "high"


def test_urgent_priority_field_maps_to_critical():
    issue = Issue(github_issue(fields=[("Priority", "Urgent")]), "org/repo")
    assert issue.priority == "critical"


def test_priority_from_label_when_field_not_set():
    issue = Issue(github_issue(labels=["priority: low"]), "org/repo")
    assert issue.priority == "low"


def test_priority_field_wins_over_priority_label():
    github = github_issue(labels=["priority: low"], fields=[("Priority", "High")])
    assert Issue(github, "org/repo").priority == "high"


def test_priority_not_set_without_field_or_label():
    assert Issue(github_issue(), "org/repo").priority == "---"


def test_effort_field_is_ignored():
    github = github_issue(fields=[("Effort", "High")])
    assert Issue(github, "org/repo").priority == "---"


def test_unknown_priority_option_warns_and_falls_back_to_label(capsys):
    github = github_issue(
        number=7, labels=["priority: low"], fields=[("Priority", "P0")]
    )
    assert Issue(github, "org/repo").priority == "low"
    warning = capsys.readouterr().err
    assert "#7" in warning
    assert "P0" in warning


def test_unknown_priority_option_without_label_is_not_set(capsys):
    github = github_issue(fields=[("Priority", "P0")])
    assert Issue(github, "org/repo").priority == "---"
    assert "label" not in capsys.readouterr().err


def test_unknown_priority_option_warns_only_once(capsys):
    issue = Issue(github_issue(fields=[("Priority", "P0")]), "org/repo")
    issue.priority, issue.priority
    assert capsys.readouterr().err.count("Warning") == 1


def test_cleared_priority_field_falls_back_to_label():
    github = github_issue(labels=["priority: low"])
    github._rawData["issue_field_values"] = [
        {"issue_field_name": "Priority", "value": None, "single_select_option": None}
    ]
    assert Issue(github, "org/repo").priority == "low"


def test_priority_mapping_to_unknown_priority_is_rejected():
    with pytest.raises(Exit):
        ReleaseNotesGenerator("o/r", "T", "I", priority_mapping={"p0": "urgent"})


def generate_release_notes(monkeypatch, issues, **config):
    milestone = SimpleNamespace(title="v1.0")
    repository = SimpleNamespace(
        full_name="org/repo",
        get_milestones=lambda state: [milestone],
        get_issues=lambda milestone, state: issues,
    )
    monkeypatch.setattr(releasenotes, "get_repository", lambda *args: repository)
    output = io.StringIO()
    generator = ReleaseNotesGenerator("org/repo", "Title", "Intro", **config)
    generator.generate(Version("1.0"), file=output)
    return output.getvalue()


def test_custom_priority_mapping(monkeypatch):
    issues = [github_issue(labels=["bug"], fields=[("Priority", "P0")])]
    notes = generate_release_notes(
        monkeypatch, issues, priority_mapping={"P0": "critical"}
    )
    assert "| bug | critical | Issue 1 |" in notes


def test_most_important_enhancements_include_priority_field_issues(monkeypatch):
    issues = [
        github_issue(1, labels=["enhancement"], fields=[("Priority", "Urgent")]),
        github_issue(2, labels=["enhancement", "priority: high"]),
        github_issue(3, labels=["enhancement"], fields=[("Priority", "Low")]),
    ]
    notes = generate_release_notes(monkeypatch, issues)
    highlights = notes.split("## Most important enhancements")[1].split("##")[0]
    assert "Issue 1" in highlights
    assert "Issue 2" in highlights
    assert "Issue 3" not in highlights


def test_custom_priority_mapping_extends_default_mapping(monkeypatch):
    issues = [github_issue(labels=["bug"], fields=[("Priority", "High")])]
    notes = generate_release_notes(
        monkeypatch, issues, priority_mapping={"P0": "critical"}
    )
    assert "| bug | high | Issue 1 |" in notes
