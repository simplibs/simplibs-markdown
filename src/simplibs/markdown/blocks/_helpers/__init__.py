# Constants
from .constants.ATTR_NAME import ATTR_NAME
from .constants.BLOCK_START import BLOCK_START
from .constants.BREAK_SUFFIX import BREAK_SUFFIX
from .constants.TAG_NAME import TAG_NAME
from .constants.VOID_TAGS import VOID_TAGS
from .constants.YAML_PLAIN_KEY import YAML_PLAIN_KEY
from .constants.YAML_RESERVED import YAML_RESERVED
# Functions
from .build_html_open_tag import build_html_open_tag
from .choose_fence import choose_fence
from .escape_block_start import escape_block_start
from .store_html_content import store_html_content
from .yaml_inline import yaml_inline
from .yaml_key import yaml_key
from .yaml_lines import yaml_lines


_DESIGN_NOTES = """
# Markdown Blocks Helpers Sub-Package

## Purpose
Private helpers and constants of the block nodes. What a second domain needs
lives in `_common/helpers`.

## Internal Components Registry

| Component                 | Type     | Description                                                       |
| :------------------------ | :------- | :---------------------------------------------------------------- |
| `ATTR_NAME`               | Constant | Pattern of a valid HTML attribute name.                           |
| `BLOCK_START`             | Constant | Pattern of a line that Markdown would read as the start of a block. |
| `BREAK_SUFFIX`            | Constant | The end of a line for each line break style.                      |
| `build_html_open_tag`     | Function | Writes the opening tag with escaped attribute values.             |
| `choose_fence`            | Function | Picks a code fence longer than any run inside the code.           |
| `escape_block_start`      | Function | Escapes a line that Markdown would read as the start of a block.  |
| `store_html_content`      | Function | Turns the content of an HTML node into inline content or blocks.  |
| `TAG_NAME`                | Constant | Pattern of a valid HTML tag name.                                 |
| `VOID_TAGS`               | Constant | HTML tags that have no closing tag and no content.                |
| `yaml_inline`             | Function | Writes a scalar or an empty collection as YAML.                   |
| `yaml_key`                | Function | Writes a dictionary key as YAML, quoted when it must be.          |
| `yaml_lines`              | Function | Writes a value as indented YAML lines.                            |
| `YAML_PLAIN_KEY`          | Constant | Pattern of a key that needs no quotes.                            |
| `YAML_RESERVED`           | Constant | Words that YAML reads as a value, so a key must be quoted.        |
"""
