"Basic Hypothesis test suite for ktane.ask."

import sys
from unittest.mock import patch
from hypothesis import given, assume, strategies as st

sys.path.append('..')
import ktane.ask #pylint: disable=wrong-import-position #directory hack

@given(st.text(), st.text())
def test_yes_no_returns_bool(prompt, answer):
    "Test that ask.yes_no returns a boolean."
    with patch("builtins.input", lambda _: answer):
        returned_answer = ktane.ask.yes_no(prompt)
        assert isinstance(returned_answer, bool)

@given(st.sets(st.text()), st.booleans(), st.data())
def test_str_from_set(inputs_set, case_sensitive, data):
    "Test that ask.str_from_set returns strings in the set passed to it."
    try:
        with patch("builtins.input", lambda _: data.draw(st.text())):
            return_string = ktane.ask.str_from_set(inputs_set,
                                                   case_sensitive=case_sensitive)
            assert return_string in inputs_set
    except RuntimeError as message:
        #expected failure if too many inputs fail
        if str(message) == "Too many invalid user inputs.":
            assume(False)
        else:
            raise

@given(st.sets(st.text()), st.booleans(), st.data())
def test_list_from_set(inputs_set, case_sensitive, data):
    """Test that ask.list_from_set returns lists
    containing only strings in the set passed to it."""
    try:
        with patch("builtins.input", lambda _: data.draw(st.text())):
            return_list = ktane.ask.list_from_set(inputs_set,
                                                  case_sensitive=case_sensitive)
            assert all(s in inputs_set for s in return_list)
    except RuntimeError as message:
        #expected failure if too many inputs fail
        if str(message) == "Too many invalid user inputs.":
            assume(False)
        else:
            raise

if __name__ == "__main__":
    ktane.ask.ENABLE_PRINTING = False #type: ignore[misc] #disable printing for the test
    test_yes_no_returns_bool()
    test_str_from_set()
    test_list_from_set()
