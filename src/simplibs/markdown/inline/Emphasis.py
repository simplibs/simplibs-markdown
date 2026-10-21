# Outers
from .._common.helpers import as_inline
from .._common.validations import raise_param_invalid_type_error
from ..base_class import InlineMarkdown
# Inners
from ._helpers import EMPHASIS_REPEAT
from ._validations.emphasis import (
    raise_emphasis_empty_inner_error,
    raise_emphasis_marker_kind_mismatch_error,
)
from .enums import EmphasisKind, EmphasisMarker


class Emphasis(InlineMarkdown):
    """Emphasis, strong text, both, or strike-through around some content.

    Args:
        inner: The content (a string, an inline node or a list of them).
        kind: What kind of emphasis it is.
        marker: The character to wrap the content with. Defaults to `*`, or
            `~` for strike-through.

    Raises:
        ParamError: If `kind` or `marker` has the wrong type, the marker does
            not fit the kind, or the content is empty.
    """

    __slots__ = ("inner", "kind", "marker")

    def __init__(
        self,
        inner,
        kind: EmphasisKind = EmphasisKind.EM,
        marker: EmphasisMarker | None = None,
    ) -> None:

        # 1. Validation
        # 1.1 The kind
        if not isinstance(kind, EmphasisKind):
            raise_param_invalid_type_error("kind", kind, EmphasisKind)

        # 1.2 The marker: the default depends on the kind
        if marker is None:
            marker = EmphasisMarker.TILDE if kind is EmphasisKind.STRIKE else EmphasisMarker.ASTERISK
        elif not isinstance(marker, EmphasisMarker):
            raise_param_invalid_type_error("marker", marker, EmphasisMarker)

        # 1.3 Only strike-through is written with a tilde
        if (kind is EmphasisKind.STRIKE) != (marker is EmphasisMarker.TILDE):
            raise_emphasis_marker_kind_mismatch_error(kind, marker)

        # 1.4 The content must have something to emphasize
        inner = as_inline(inner)
        inner_text = inner.to_text()
        if not inner_text.strip():
            raise_emphasis_empty_inner_error(inner_text)

        # 2. Assignment
        self.inner = inner
        self.kind = kind
        self.marker = marker

    def to_inline(self) -> str:

        # 1. Whitespace at the edges would make the markers fail, so it moves outside
        text = self.inner.to_text()
        core = text.strip()
        lead = text[: len(text) - len(text.lstrip())]
        trail = text[len(text.rstrip()):]

        # 2. Wrap the content in the marker, repeated as often as the kind needs
        mark = self.marker.value * EMPHASIS_REPEAT[self.kind]
        return f"{lead}{mark}{core}{mark}{trail}"


_DESIGN_NOTES = """
# Emphasis — Four Kinds, One Node

## Purpose
Emphasis, strong, both and strike-through are one mechanism: a marker
repeated around content. The kind chooses how often (`EMPHASIS_REPEAT`).

## Edge Whitespace Moves Out
`** text **` is not strong text in CommonMark. The leading and trailing
whitespace of the content is written outside the markers, so the result is
`  **text**  ` and always works.

## Added Since the Draft
A check that `marker` is an `EmphasisMarker`; without it a string would only
fail later with an `AttributeError`.

## Known Limit
An underscore marker does not work inside a word (`snake_case`). The node
does not see the text around it, so it cannot warn about that.
"""
