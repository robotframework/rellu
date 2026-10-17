# rellu

Tooling for creating releases of GitHub projects and generating their release notes from the issue tracker.

## Issue metadata

**Issue field**:
A structured value defined at the GitHub organization level and attached to an issue, such as Priority or Effort.
_Avoid_: Field label, custom field

**Label**:
A free-form tag on an issue in a single repository.
_Avoid_: Field, tag

**Priority field**:
The organization-level issue field that holds an issue's priority as one of a set of options.
_Avoid_: Priority label

**Priority label**:
A label of the form `priority: <level>` that records an issue's priority without using issue fields.
_Avoid_: Priority field

**Priority**:
The issue's priority as rellu resolves it: critical, high, medium, low, or not set. It comes from the Priority field when that is set, and otherwise from a priority label.
_Avoid_: Prio

**Effort field**:
The organization-level issue field that records how much work an issue takes. It plays no part in release notes.
