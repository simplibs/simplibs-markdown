import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.containers._validations.quote import (
    raise_quote_unknown_alert_error,
)


@pytest.mark.parametrize("alert", ["NOTE", "tip", 1, None])
def test_raise_quote_unknown_alert_error_contract(subtests, alert) -> None:
    """Verify raise_quote_unknown_alert_error produces a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_quote_unknown_alert_error,
        invalid_params=(alert,),
        exception_type=ParamError,
        error_name="MARKDOWN_QUOTE_UNKNOWN_ALERT",
        label="quote alert",
        expected="An AlertKind member: NOTE, TIP, IMPORTANT, WARNING or CAUTION.",
        value=alert,
        problem="Only the five alert kinds of GitHub are known.",
        how_to_fix=(
            "Pass one of the `AlertKind` members.",
            "Leave `alert` out for a plain quote.",
        ),
        exception=TypeError,
        verbose=False,
    )
