"Hypothesis strategies for generating project-specific objects."

import sys
from typing import Any
from hypothesis import strategies as st

sys.path.append('..')
from ktane.directors import Edgework, Port, EdgeFlag  # noqa: E402


@st.composite
def serial_numbers(draw: Any) -> Any:  # todo: optimize with st.permutations
    "Strategy to generate valid serial numbers."
    return draw(st.text(
        alphabet=st.characters(whitelist_categories=('Ll', 'Nd')),
        min_size=6, max_size=6
    ).filter(lambda s: not (s.isalpha() or s.isdigit())))


@st.composite
def port_plate_lists(draw: Any) -> Any:
    "Strategy to generate tuples matching ktane.directors.PortPlateList."
    port_list = draw(st.lists(st.lists(st.sampled_from(Port))))
    return tuple(tuple(plate) for plate in port_list)


@st.composite
def indicator_lists(draw: Any) -> Any:
    "Strategy to generate tuples matching ktane.directors.IndicatorList."
    ind_list = draw(st.lists(st.tuples(
        st.from_regex(r'[a-z]{3}|[A-Z]{3}'),
        st.booleans()
    )))
    return tuple(ind_list)


@st.composite
def edgeworks(draw: Any) -> Any:
    "Strategy to generate ktane.directors.Edgework objects."
    new_edgework = Edgework()
    new_edgework.set_edgeflags(tuple(draw(st.lists(st.sampled_from(EdgeFlag)))))
    new_edgework.post_init(
        start_time_mins=draw(st.integers(min_value=1)),
        total_modules=draw(st.integers()),
        max_strikes=draw(st.integers(min_value=1)),
        batteries=draw(st.integers(min_value=0)),
        indicators=draw(indicator_lists()),
        port_plates=draw(port_plate_lists()),
        serial=draw(serial_numbers()),
        strikes=draw(st.integers()),
        solves=draw(st.integers())
    )
