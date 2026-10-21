# Outers
from ..base_class import InlineMarkdown
from .._common.validations import raise_param_invalid_type_error
# Inners
from ._helpers import REFERENCE_FORMS
from ._validations.reference import raise_reference_invalid_value_error
from .enums import ReferenceKind


class Reference(InlineMarkdown):
    """An automatic reference: a mention, an issue, a commit or an emoji.

    Args:
        kind: The kind of the reference.
        value: The value without the leading mark (`"octocat"`, `12`). A string
            or an integer; a bool is not accepted.

    Raises:
        ParamError: If `kind` or `value` has the wrong type, or `value` does not
            fit the kind.
    """

    __slots__ = ("kind", "value")

    def __init__(self, kind: ReferenceKind, value: str | int) -> None:

        # 1. Validation
        # 1.1 The kind
        if not isinstance(kind, ReferenceKind):
            raise_param_invalid_type_error("kind", kind, ReferenceKind)

        # 1.2 The type of the value is checked first, because `str(None)` or `str(True)`
        #     would pass for text and give `@None` or `@True`
        if isinstance(value, bool) or not isinstance(value, (str, int)):
            raise_param_invalid_type_error("value", value, "str | int")

        # 1.3 The text of the value fits the kind
        pattern, _, expected = REFERENCE_FORMS[kind]
        if not pattern.fullmatch(str(value)):
            raise_reference_invalid_value_error(kind, value, expected)

        # 2. Assignment
        self.kind = kind
        self.value = str(value)

    def to_inline(self) -> str:

        # 1. The template of the kind adds the mark (`@`, `#`, `:...:`)
        _, template, _ = REFERENCE_FORMS[self.kind]
        return template.format(self.value)


_DESIGN_NOTES = """
# Reference — Text That the Platform Links

## Purpose
`@octocat`, `#12`, `owner/repo#12` are plain text in CommonMark and links on
GitHub. The node checks the shape, so `@some user` is an error and not a
mention that silently never links.

## One Table
Everything that differs between the kinds is in `REFERENCE_FORMS`; this file
has no branch per kind.

## The Value Is a String or an Integer
An issue number is naturally an integer (`12`), so integers are accepted and
written with `str()`. Nothing else is: the pattern is checked against
`str(value)`, and `str(None)` or `str(True)` are the words `None` and `True`,
which fit the shape of a username and would give `@None` and `@True`. The
type is therefore checked before the shape, and a `bool` is refused even
though it is an `int`.

## Not `Text`
`Text` escapes a leading `#`, so `#12` written as a string would become
`\\#12` and never link. A reference has to stay a reference.
"""
