"Modded modules whose names begin with the letter W."

from typing import Final

from ktane.directors import ModuleSolver
from ktane.ask import talk
from ktane import ask

__all__ = [
    "WordScramble",
]


class WordScramble(ModuleSolver):
    "Solver for Word Scramble."
    name: Final = "Word Scramble"
    id: Final = "WordScrambleModule"
    required_edgework: Final = ()

    words: Final = {"module", "ottawa", "banana", "kaboom", "letter", "widget",
                    "person", "sapper", "wiring", "archer", "device", "rocket",
                    "damage", "defuse", "flames", "semtex", "cannon", "blasts",
                    "attack", "weapon", "charge", "napalm", "mortar", "bursts",
                    "casing", "disarm", "keypad", "button", "robots", "kevlar"}

    def stage(self) -> None:
        talk("What is displayed on the module?")
        scramble = ask.str_from_regex(r"[a-z]{6}")
        while set(scramble) not in [set(w) for w in self.words]:
            talk("Those letters don't correspond to a known word.")
            talk("What is displayed on the module?")
            scramble = ask.str_from_regex(r"[a-z]{6}")
        answer = [w for w in self.words if set(w) == set(scramble)][0]
        talk(f'Type in the word "{answer}".')
