"Mock versions of things for isolated testing."

from typing import Final, Callable, List, AbstractSet
from hypothesis import strategies as st


class MockAsk:
    "Mock of the ktane.ask module."

    ENABLE_PRINTING: Final = True
    PROMPT: Final = "> "
    SEPARATOR: Final = ", "
    MAX_LINE_PRINT_LENGTH: Final = 80

    def __init__(self, data: st.DataObject) -> None:
        self._data = data

    def talk(self, message: str = "", /, *, warning_bypass: bool = False) -> None:
        pass

    def yes_no(self, prompt: str, /) -> bool:
        return self._data.draw(st.booleans())

    def list_from_func(self, func: Callable[[str], bool], *, case_sensitive: bool = False, expected_len: int = 0) -> List[str]:
        if not case_sensitive:
            if expected_len == 0:
                return self._data.draw(st.lists(st.text().map(str.lower).filter(func)))
            return self._data.draw(st.lists(st.text().map(str.lower).filter(func), min_size=expected_len, max_size=expected_len))
        if expected_len == 0:
            return self._data.draw(st.lists(st.text().filter(func)))
        return self._data.draw(st.lists(st.text().filter(func), min_size=expected_len, max_size=expected_len))

    def str_from_func(self, func: Callable[[str], bool], *, case_sensitive: bool = False) -> str:
        if not case_sensitive:
            return self._data.draw(st.text().map(str.lower).filter(func))
        return self._data.draw(st.text().filter(func))

    def list_from_set(self, valid_inputs: AbstractSet[str], *, case_sensitive: bool = False, print_options: bool = False, expected_len: int = 0) -> List[str]:
        if not case_sensitive:
            if expected_len == 0:
                return self._data.draw(st.lists(st.sampled_from([s.lower() for s in valid_inputs])))
            return self._data.draw(st.lists(st.sampled_from([s.lower() for s in valid_inputs]), min_size=expected_len, max_size=expected_len))
        if expected_len == 0:
            return self._data.draw(st.lists(st.sampled_from(list(valid_inputs))))
        return self._data.draw(st.lists(st.sampled_from(list(valid_inputs)), min_size=expected_len, max_size=expected_len))

    def str_from_set(self, valid_inputs: AbstractSet[str], *, case_sensitive: bool = False, print_options: bool = False) -> str:
        if not case_sensitive:
            return self._data.draw(st.sampled_from([s.lower() for s in valid_inputs]))
        return self._data.draw(st.sampled_from(list(valid_inputs)))

    def list_from_regex(self, input_pattern: str, *, case_sensitive: bool = False, expected_len: int = 0) -> List[str]:
        if not case_sensitive:
            if expected_len == 0:
                return self._data.draw(st.lists(st.from_regex(input_pattern, fullmatch=True).filter(str.islower)))
            return self._data.draw(st.lists(st.from_regex(input_pattern, fullmatch=True).filter(str.islower), min_size=expected_len, max_size=expected_len))
        if expected_len == 0:
            return self._data.draw(st.lists(st.from_regex(input_pattern, fullmatch=True)))
        return self._data.draw(st.lists(st.from_regex(input_pattern, fullmatch=True), min_size=expected_len, max_size=expected_len))

    def str_from_regex(self, input_pattern: str, *, case_sensitive: bool = False) -> str:
        if not case_sensitive:
            return self._data.draw(st.from_regex(input_pattern, fullmatch=True).filter(str.islower))
        return self._data.draw(st.from_regex(input_pattern, fullmatch=True))

    def positive_int(self) -> int:
        return self._data.draw(st.integers(min_value=1))


def mock_talk(message: str = "", /, *, warning_bypass: bool = False) -> None:
    "Standalone mock of ktane.ask.talk."
