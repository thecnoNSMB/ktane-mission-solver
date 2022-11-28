"""Modded modules whose names begin with the letter W."""

from typing import Final

from ktane import ask
from ktane.directors import ModuleSolver

__all__ = [
    "WordScramble",
]


class WordScramble(ModuleSolver):
    """Solver for Word Scramble."""

    name: Final = "Word Scramble"
    id: Final = "WordScrambleModule"
    required_edgework: Final = ()

    words: Final = {
        "module",
        "ottawa",
        "banana",
        "kaboom",
        "letter",
        "widget",
        "person",
        "sapper",
        "wiring",
        "archer",
        "device",
        "rocket",
        "damage",
        "defuse",
        "flames",
        "semtex",
        "cannon",
        "blasts",
        "attack",
        "weapon",
        "charge",
        "napalm",
        "mortar",
        "bursts",
        "casing",
        "disarm",
        "keypad",
        "button",
        "robots",
        "kevlar",
    }

    def stage(self) -> None:
        ask.talk("What is displayed on the module?")
        scramble = ask.str_from_regex(r"[a-z]{6}")
        while set(scramble) not in {set(word) for word in self.words}:
            ask.talk("Those letters don't correspond to a known word.")
            ask.talk("What is displayed on the module?")
            scramble = ask.str_from_regex(r"[a-z]{6}")
        answer = [word for word in self.words if set(word) == set(scramble)][0]
        ask.talk('Type in the word "{0}".'.format(answer))
