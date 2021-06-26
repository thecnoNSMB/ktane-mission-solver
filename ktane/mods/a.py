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

    words: Final = {"stream", "master", "tamers", "looped", "poodle", "pooled",
                    "cellar", "caller", "recall", "seated", "sedate", "teased",
                    "rescue", "secure", "recuse", "rashes", "shears", "shares",
                    "barely", "barley", "bleary", "duster", "rusted", "rudest"}

    def stage(self) -> None:
        talk("What word is on the display?")
        word = ask.str_from_set(self.words)
        anagrams = [w for w in self.words if set(w) == set(word) and w != word]
        talk(f'Type in the word "{anagrams[0]}"')
