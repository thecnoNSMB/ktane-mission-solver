"Modded modules whose names begin with the letter C."

from typing import Final

from ktane.directors import ModuleSolver
from ktane.ask import talk
from ktane import ask

__all__ = [
    "ColourFlash",
]

class ColourFlash(ModuleSolver):
    "Solver for Colour Flash."
    name: Final = "Colour Flash"
    required_edgework: Final = ()

    valid_colors: Final = {"red", "yellow", "green", "blue", "magenta", "white"}

    def stage(self) -> None:
        talk("What color is the last word in the sequence?")
        last_color = ask.str_from_set(self.valid_colors, print_options=True)
