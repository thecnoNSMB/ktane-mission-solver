"""Basic Hypothesis test suite for ktane.directors."""

from typing import List
from unittest.mock import patch

from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st
from mocks import MockAsk, mock_talk

from ktane import directors


@given(st.lists(st.sampled_from(directors.EdgeFlag)), st.data())
@settings(suppress_health_check=(HealthCheck.filter_too_much,))
def test_edgework(edgeflags: List[directors.EdgeFlag], data_obj: st.DataObject) -> None:
    """Test that ktane.edgework does not break under proper initialization."""
    edgework = directors.Edgework()
    edgework.set_edgeflags(tuple(edgeflags))
    with patch("ktane.directors.ask", MockAsk(data_obj)):
        with patch("ktane.directors.talk", mock_talk):
            edgework.post_init()
    assert isinstance(edgework.hit_strike_limit, bool)
    assert isinstance(edgework.defused, bool)
    assert isinstance(edgework.serial_odd, bool)
    assert isinstance(edgework.serial_vowel, bool)
    assert isinstance(edgework.serial_first_digit, str)
    assert isinstance(edgework.serial_first_letter, str)


if __name__ == "__main__":
    test_edgework()
