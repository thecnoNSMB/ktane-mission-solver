"Modded modules whose names begin with the letter A."

from typing import Final

from ktane.directors import ModuleSolver
from ktane.ask import talk
from ktane import ask

__all__ = [
    "Anagrams",
]

class Anagrams(ModuleSolver):
    "Solver for Anagrams."
    name: Final = "Anagrams"
    id: Final = "AnagramsModule"
    required_edgework: Final = ()
