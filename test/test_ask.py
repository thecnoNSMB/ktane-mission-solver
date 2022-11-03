"Basic Hypothesis test suite for ktane.ask."

import sys
from typing import Set
from unittest.mock import patch
from hypothesis import given, assume, strategies as st

sys.path.append('..')  # TODO: don't?
from ktane import ask  # noqa: E402


@given(st.sets(st.text()), st.booleans(), st.booleans(), st.data())
def test_str_from_set(inputs_set: Set[str], case_sensitive: bool, print_options: bool,
                      data: st.DataObject) -> None:
    "Test that ask.str_from_set returns strings in the set passed to it."
    try:
        with patch("builtins.input", lambda _: data.draw(st.text())):
            return_string = ask.str_from_set(inputs_set, case_sensitive=case_sensitive,
                                             print_options=print_options)
            assert return_string in inputs_set
    except RuntimeError as message:
        # expected failure if too many inputs fail
        if str(message) == "Too many invalid user inputs.":
            assume(False)
        else:
            raise


@given(st.sets(st.text()), st.booleans(), st.booleans(), st.integers(), st.data())
def test_list_from_set(inputs_set: Set[str], case_sensitive: bool, print_options: bool,
                       expected_len: int, data: st.DataObject) -> None:
    """Test that ask.list_from_set returns lists
    containing only strings in the set passed to it."""
    try:
        with patch("builtins.input", lambda _: data.draw(st.text())):
            return_list = ask.list_from_set(inputs_set, case_sensitive=case_sensitive,
                                            print_options=print_options,
                                            expected_len=expected_len)
            assert all(s in inputs_set for s in return_list)
    except RuntimeError as message:
        # expected failure if too many inputs fail
        if str(message) == "Too many invalid user inputs.":
            assume(False)
        else:
            raise


@given(st.data())
def test_positive_int(data: st.DataObject) -> None:
    "Test that ask.positive_int actually returns positive nonzero integers."
    try:
        with patch("builtins.input", lambda _: data.draw(st.sampled_from('0123456789'))):
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
