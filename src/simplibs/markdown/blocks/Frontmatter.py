# Outers
from ..base_class import Markdown
from ..base_class.enums import NodeLevel
from .._common.validations import raise_param_invalid_type_error
# Inners
from ._helpers import yaml_lines


class Frontmatter(Markdown):
    """A YAML header between two `---` lines, for the start of a document.

    Args:
        data: The header as a dictionary. Values: strings, numbers, bools,
            `None`, and lists or dictionaries of them. Keys: strings. An empty
            dictionary gives an empty header: two `---` lines and nothing between.

    Raises:
        ParamError: If `data` is not a dictionary.
        ConversionError: If a value or a key cannot be written as YAML.
    """

    __slots__ = ("data", "lines")

    node_level = NodeLevel.BLOCK

    def __init__(self, data: dict) -> None:

        # 1. Validation
        if not isinstance(data, dict):
            raise_param_invalid_type_error("data", data, dict)

        # 2. Write the header now, so an unsupported value fails here; no keys, no `{}`
        body = yaml_lines(data) if data else ()
        lines = ("---", *body, "---")

        # 3. Assignment
        self.data = data
        self.lines = lines

    def to_lines(self) -> tuple[str, ...]:

        # 1. The lines written at construction
        return self.lines


_DESIGN_NOTES = """
# Frontmatter — Metadata at the Top of a File

## Purpose
`---`, a few keys, `---`. Static site generators, Obsidian and GitHub read it.

## Written at Construction
The draft wrote the YAML in `to_lines()`, so an unsupported value failed in
the middle of writing a file. Now the header is written once in the
constructor and the error appears where the data is passed. The cost: a
change to the dictionary afterwards is not reflected in the output.

## An Empty Dictionary Is an Empty Header
`yaml_lines({})` gives `{}`, which is right for a value (`tags: {}`) but not
for the whole header: `---`, `{}`, `---` is valid YAML and pure noise. A
header built from data sometimes ends up with no keys, so `Frontmatter({})`
writes the two marker lines and nothing between them. An empty value inside
the header (`{"tags": []}`) is still written on the line of its key.

## Not a General YAML Writer
See `yaml_lines`: a small, readable writer for plain data.
"""
