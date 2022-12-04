"""Utilities for asking for and processing Morse Code signals."""

from types import MappingProxyType
from typing import Final

from ktane import ask

__all__ = ["valid_morse", "decode", "ask_word"]

MORSE_ALPHABET: Final = MappingProxyType({
    "a": ".-",
    "b": "-...",
    "c": "-.-.",
    "d": "-..",
    "e": ".",
    "f": "..-.",
    "g": "--.",
    "h": "....",
    "i": "..",
    "j": ".---",
    "k": "-.-",
    "l": ".-..",
    "m": "--",
    "n": "-.",
    "o": "---",
    "p": ".--.",
    "q": "--.-",
    "r": ".-.",
    "s": "...",
    "t": "-",
    "u": "..-",
    "v": "...-",
    "w": ".--",
    "x": "-..-",
    "y": "-.--",
    "z": "--..",
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
})

INVERSE_MORSE_ALPHABET: Final = MappingProxyType({
    morse: char for char, morse in MORSE_ALPHABET.items()
})


def valid_morse(text: str) -> bool:
    """Determine whether a string is valid Morse code."""
    chars = text.split()
    return all(char in INVERSE_MORSE_ALPHABET for char in chars)


def decode(code: str) -> str:
    """Convert a Morse code string into regular text."""
    chars = code.split()
    return "".join(INVERSE_MORSE_ALPHABET[char] for char in chars)


def ask_word() -> str:
    """Get a Morse code string from the user and convert it to a word."""
    code = ask.str_from_func(valid_morse)
    return decode(code)
