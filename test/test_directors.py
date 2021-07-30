"Basic Hypothesis test suite for ktane.directors."

import sys
from unittest.mock import patch
from typing import List
from hypothesis import given, strategies as st
from mocks import MockAsk, mock_talk #type: ignore

sys.path.append('..')
from ktane import directors #pylint: disable=wrong-import-position, wrong-import-order

@given(st.lists(st.sampled_from(directors.EdgeFlag)), st.data())
def test_edgework(edgeflags: List[directors.EdgeFlag], data: st.DataObject) -> None:
    "Test that ktane.edgework does not break under proper initialization."
    edgework = directors.Edgework()
    edgework.set_edgeflags(tuple(edgeflags))
    with patch('ktane.directors.ask', MockAsk(data)), \
         patch('ktane.directors.talk', mock_talk):
        edgework.post_init()

if __name__ == "__main__":
    test_edgework()
