import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown._common.validations import raise_node_not_markdown_error


@pytest.mark.parametrize("value", [42, 3.14, None, True, ["a"], {"a": 1}])
def test_raise_node_not_markdown_error_contract(subtests, value) -> None:
    """Verify raise_node_not_markdown_error produces a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_node_not_markdown_error,
        invalid_params=(value,),
        exception_type=ParamError,
        error_name="MARKDOWN_NODE_NOT_MARKDOWN",
        label="content",
        expected="A string or a Markdown node (Text, Heading, Paragraph...).",
        value=value,
        problem="This value cannot be turned into Markdown.",
        how_to_fix=(
            "Pass a string, or build the node with the matching class.",
            "Convert other values with str() first.",
        ),
        exception=TypeError,
        verbose=False,
    )
