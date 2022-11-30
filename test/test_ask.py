"""Basic Hypothesis test suite for ktane.ask."""

from string import digits as digits_str
from typing import Set
from unittest.mock import patch

from hypothesis import assume, given
from hypothesis import strategies as st

from ktane import ask


@given(st.sets(st.text()), st.booleans(), st.booleans(), st.data())
def test_str_from_set(
    inputs_set: Set[str],
    case_sensitive: bool,
    print_options: bool,
    data_obj: st.DataObject,
) -> None:
    """Test that ask.str_from_set returns strings in the set passed to it."""
    try:
        with patch("builtins.input", lambda _: data_obj.draw(st.text())):
            return_string = ask.str_from_set(
                inputs_set, case_sensitive=case_sensitive, print_options=print_options,
            )
            # TODO: breaks when case-insensitive
            assert return_string in inputs_set
    except RuntimeError as message:
        # expected failure if too many inputs fail
        if str(message) == "Too many invalid user inputs.":
            assume(False)
        else:
            raise


@given(st.sets(st.text()), st.booleans(), st.booleans(), st.integers(), st.data())
def test_list_from_set(
    inputs_set: Set[str],
    case_sensitive: bool,
    print_options: bool,
    expected_len: int,
    data_obj: st.DataObject,
) -> None:
    """
    Test that ask.list_from_set returns lists
    containing only strings in the set passed to it.
    """
    try:
        with patch("builtins.input", lambda _: data_obj.draw(st.text())):
            return_list = ask.list_from_set(
                inputs_set,
                case_sensitive=case_sensitive,
                print_options=print_options,
                expected_len=expected_len,
            )
            assert all(string in inputs_set for string in return_list)
    except RuntimeError as message:
        # expected failure if too many inputs fail
        if str(message) == "Too many invalid user inputs.":
            assume(False)
        else:
            raise


@given(st.data())
def test_positive_int(data_obj: st.DataObject) -> None:
    """Test that ask.positive_int actually returns positive nonzero integers."""
    try:
        with patch(
            "builtins.input", lambda _: data_obj.draw(st.sampled_from(digits_str)),
        ):
            return_int = ask.positive_int()
            assert return_int > 0
    except RuntimeError as message:
        # expected failure if too many inputs fail
        if str(message) == "Too many invalid user inputs.":
            assume(False)
        else:
            raise


if __name__ == "__main__":
    ask.ENABLE_PRINTING = False  # type: ignore[misc] #disable printing for the test
    test_str_from_set()
    test_list_from_set()
    test_positive_int()
