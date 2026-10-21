import re
from types import MappingProxyType
from typing import Final
# Outers
from simplibs.markdown.inline.enums import ReferenceKind


REFERENCE_FORMS: Final = MappingProxyType({
    ReferenceKind.MENTION: (
        re.compile(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}"),
        "@{}",
        "A GitHub username: letters, digits and '-', up to 39 characters, starting with a letter or a digit.",
    ),
    ReferenceKind.TEAM: (
        re.compile(r"[A-Za-z0-9-]+/[A-Za-z0-9_-]+"),
        "@{}",
        "An organization and a team: 'org/team-name'.",
    ),
    ReferenceKind.ISSUE: (
        re.compile(r"\d+"),
        "#{}",
        "A number, e.g. 12.",
    ),
    ReferenceKind.REPO_ISSUE: (
        re.compile(r"[\w.-]+/[\w.-]+#\d+"),
        "{}",
        "A repository and a number: 'owner/repo#12'.",
    ),
    ReferenceKind.COMMIT: (
        re.compile(r"[0-9a-f]{7,40}"),
        "{}",
        "A lowercase hexadecimal hash of 7 to 40 characters.",
    ),
    ReferenceKind.EMOJI: (
        re.compile(r"[a-z0-9_+-]+"),
        ":{}:",
        "A lowercase emoji name without colons, e.g. 'tada'.",
    ),
})
"""For each `ReferenceKind`: the pattern of a valid value, the template it is written with, and a description of the valid form (read-only)."""


_DESIGN_NOTES = """
# REFERENCE_FORMS — Everything That Differs Between the Kinds

## Purpose
Six kinds, one node. What differs is a pattern, a template and the sentence
that explains the pattern to a user whose value was rejected. They sit in one
table, so adding a kind is one entry and one enum member.

## The Third Item
The description is passed to `raise_reference_invalid_value_error`, so the
knowledge of what a valid value looks like exists in one place only.

## Limit
The patterns check the shape, not whether the user or the issue exists.
"""
