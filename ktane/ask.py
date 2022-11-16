"""Handles simple text-based I/O operations for the KTaNE solving toolkit."""

from re import fullmatch
from textwrap import wrap
from typing import AbstractSet, Callable, Final, List
from warnings import warn

__all__ = [
    "PROMPT",
    "SEPARATOR",
    "talk",
    "yes_no",
    "list_from_func",
    "str_from_func",
    "list_from_set",
    "str_from_set",
    "list_from_regex",
    "str_from_regex",
]

ENABLE_PRINTING: Final = True
PROMPT: Final = "> "
SEPARATOR: Final = ", "
# Making this larger is fine, but making it smaller may trigger warnings.
MAX_LINE_PRINT_LENGTH: Final = 80
# Debug stuff.
_MAX_ITERATIONS: Final = 20


def _from_func(
    func: Callable[[str], bool], *, case_sensitive: bool, allow_empty: bool,
) -> str:
    """
    Get a single string from the user that satisfies func,
    respecting case_sensitive and allow_empty options.
    """
    count = 0
    response = input(PROMPT)  # noqa: WPS421
    if not case_sensitive:
        response = response.lower()
    while not (func(response) or (allow_empty and response == "")):
        talk(
            'Answer "{0}" is not a valid answer and will be ignored.'.format(response),
            warning_bypass=True,
        )
        talk("Please try again.")
        count += 1
        if count >= _MAX_ITERATIONS:
            raise RuntimeError("Too many invalid user inputs.")
        response = input(PROMPT)  # noqa: WPS421
        if not case_sensitive:
            response = response.lower()
    return response


def _print_case(case_sensitive: bool) -> None:
    """Print case sensitive warning if needed."""
    if case_sensitive:
        talk("(Inputs are case sensitive.)")


def _print_set(strings: AbstractSet[str], *, case_sensitive: bool = False) -> None:
    """Display a set in readable form across one or more lines."""
    if not strings:  # empty set
        return
    if not case_sensitive:
        strings = {string.upper() for string in strings}
    for string in strings:
        if len(string) >= MAX_LINE_PRINT_LENGTH:
            warn('WARNING: String in set too long: "{0}"'.format(string))
    paragraph: str = SEPARATOR.join(sorted(strings))
    lines: List[str] = wrap(paragraph, width=MAX_LINE_PRINT_LENGTH)
    for line in lines:
        talk(line)


def talk(message: str = "", *, warning_bypass: bool = False) -> None:
    """Mainly here so that output can be disabled for testing."""
    if not warning_bypass and len(message) > MAX_LINE_PRINT_LENGTH:
        warn('WARNING: Message too long: "{0}"'.format(message))
    if ENABLE_PRINTING:
        print(message)  # noqa: WPS421


def yes_no(prompt: str) -> bool:
    """Ask the user a yes/no question."""
    prompt = "{0} (y/n) ".format(prompt)
    if len(prompt) > MAX_LINE_PRINT_LENGTH:
        warn('WARNING: Prompt too long: "{0}"'.format(prompt))
    return input(prompt).strip().lower() == "y"  # noqa: WPS421


def list_from_func(
    func: Callable[[str], bool], *, case_sensitive: bool = False, expected_len: int = 0,
) -> List[str]:
    """
    Prompt the user to enter a list of strings
    which when passed to func all return True.
    """
    _print_case(case_sensitive)
    responses: List[str] = []
    if expected_len > 0:
        talk("(One per line.)")
        while len(responses) < expected_len:
            responses.append(_from_func(func, case_sensitive=case_sensitive))
    else:
        talk("(One per line. End inputs by hitting ENTER without giving input.)")
        ans = _from_func(func, case_sensitive=case_sensitive, allow_empty=True)
        while ans:
            responses.append(ans)
            ans = _from_func(func, case_sensitive=case_sensitive, allow_empty=True)
    return responses


def str_from_func(func: Callable[[str], bool], *, case_sensitive: bool = False) -> str:
    """Prompt the user to enter a string which when passed to func returns True."""
    _print_case(case_sensitive)
    return _from_func(func, case_sensitive=case_sensitive)


def list_from_set(
    valid_strings: AbstractSet[str], *,
    case_sensitive: bool = False,
    print_options: bool = False,
    expected_len: int = 0,
) -> List[str]:
    """Prompt the user to enter a list of strings from valid_strings."""
    if print_options:
        talk("Accepted options are:")
        _print_set(valid_strings, case_sensitive=case_sensitive)
    if not case_sensitive:  # normalize
        valid_strings = {string.lower() for string in valid_strings}
    return list_from_func(
        lambda string: string in valid_strings,
        case_sensitive=case_sensitive,
        expected_len=expected_len,
    )


def str_from_set(
    valid_strings: AbstractSet[str], *,
    case_sensitive: bool = False,
    print_options: bool = False,
) -> str:
    """Prompt the user to enter a string from valid_strings."""
    if print_options:
        talk("Accepted options are:")
        _print_set(valid_strings, case_sensitive=case_sensitive)
    if not case_sensitive:  # normalize
        valid_strings = {string.lower() for string in valid_strings}
    return str_from_func(
        lambda string: string in valid_strings, case_sensitive=case_sensitive,
    )


def list_from_regex(
    input_pattern: str, *, case_sensitive: bool = False, expected_len: int = 0,
) -> List[str]:
    """Prompt the user to enter a list of strings which match the input pattern."""
    return list_from_func(
        lambda string: bool(fullmatch(input_pattern, string)),
        case_sensitive=case_sensitive,
        expected_len=expected_len,
    )


def str_from_regex(input_pattern: str, *, case_sensitive: bool = False) -> str:
    """Prompt the user to enter a string which matches the input pattern."""
    return str_from_func(
        lambda string: bool(fullmatch(input_pattern, string)),
        case_sensitive=case_sensitive,
    )


# more specific ask functions


def positive_int() -> int:
    """Prompt the user to enter a positive integer (excluding 0)."""
    return int(str_from_regex(r"[1-9][0-9]*"))
