import re


def choose_code_delimiter(code: str) -> tuple[str, str]:
    """Pick the backtick run that fits a piece of inline code.

    Args:
        code: The code, without line breaks.

    Returns:
        A pair `(delimiter, body)`: the backticks to write on both sides, and
        the code, padded with a space on each side when the delimiter needs it.
    """

    # 1. The delimiter is one backtick longer than the longest run inside the code
    longest = max((len(run) for run in re.findall(r"`+", code)), default=0)
    delimiter = "`" * (longest + 1)

    # 2. Padding keeps a backtick at the edge from merging with the delimiter,
    #    and keeps a code with spaces on both sides from losing them
    needs_padding = (
        code.startswith("`")
        or code.endswith("`")
        or (code.startswith(" ") and code.endswith(" ") and code.strip(" ") != "")
    )
    return delimiter, (f" {code} " if needs_padding else code)


_DESIGN_NOTES = """
# choose_code_delimiter — Code That Contains Backticks

## Purpose
`` a`b `` needs a delimiter of two backticks, and ``` ``a`` ``` of three.
Counting the longest run inside the code is the whole algorithm.

## Padding
CommonMark removes one space on each side when both exist. The padding is
therefore added when the code starts or ends with a backtick, and when it
starts and ends with a space (so those spaces survive). Code made only of
spaces is left alone, because CommonMark does not strip it.
"""
