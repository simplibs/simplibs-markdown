from enum import Enum


class ReferenceKind(Enum):
    """The kind of an automatic reference that GitHub turns into a link."""

    MENTION = "mention"
    TEAM = "team"
    ISSUE = "issue"
    REPO_ISSUE = "repo_issue"
    COMMIT = "commit"
    EMOJI = "emoji"


_DESIGN_NOTES = """
# ReferenceKind — Text That a Platform Links by Itself

## Purpose
These are plain text in CommonMark; GitHub-flavoured renderers recognize the
shape and link it. The shape of each kind is kept next to the node that
validates it.

## Members
* `MENTION` — `@user`.
* `TEAM` — `@org/team`.
* `ISSUE` — `#12`.
* `REPO_ISSUE` — `owner/repo#12`.
* `COMMIT` — a hexadecimal hash.
* `EMOJI` — `:name:`.
"""
