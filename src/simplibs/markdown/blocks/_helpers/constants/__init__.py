_DESIGN_NOTES = """
# Markdown Blocks Helpers Sub-Package

## Purpose
Private constants of the block nodes. 

## Internal Components Registry

| Component                 | Type     | Description                                                       |
| :------------------------ | :------- | :---------------------------------------------------------------- |
| `ATTR_NAME`               | Constant | Pattern of a valid HTML attribute name.                           |
| `BLOCK_START`             | Constant | Pattern of a line that Markdown would read as the start of a block. |
| `BREAK_SUFFIX`            | Constant | The end of a line for each line break style.                      |
| `TAG_NAME`                | Constant | Pattern of a valid HTML tag name.                                 |
| `VOID_TAGS`               | Constant | HTML tags that have no closing tag and no content.                |
| `YAML_PLAIN_KEY`          | Constant | Pattern of a key that needs no quotes.                            |
| `YAML_RESERVED`           | Constant | Words that YAML reads as a value, so a key must be quoted.        |
"""
