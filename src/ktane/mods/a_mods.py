"""Modded modules whose names begin with the letter A."""

from typing import Final

from ktane import ask
from ktane.directors import ModuleSolver

__all__ = [
    "Anagrams",
]


class Anagrams(ModuleSolver):
    """Solver for Anagrams."""

    name: Final = "Anagrams"
    id: Final = "AnagramsModule"
    required_edgework: Final = ()

    words: Final = {
        "stream",
        "master",
        "tamers",
        "looped",
        "poodle",
        "pooled",
        "cellar",
        "caller",
        "recall",
        "seated",
        "sedate",
        "teased",
        "rescue",
        "secure",
        "recuse",
        "rashes",
        "shears",
        "shares",
        "barely",
        "barley",
        "bleary",
        "duster",
        "rusted",
        "rudest",
    }

    def stage(self) -> None:
        ask.talk("What word is on the display?")
        word = ask.str_from_set(self.words)
        for possible_word in self.words:
            if set(possible_word) == set(word) and possible_word != word:
                ask.talk('Type in the word "{0}".'.format(possible_word))
