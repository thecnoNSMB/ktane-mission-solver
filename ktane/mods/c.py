"Modded modules whose names begin with the letter C."

from typing import Final

from ktane.directors import ModuleSolver

__all__ = [
    "ColourFlash",
]

class ColourFlash(ModuleSolver):
    "Solver for Colour Flash."
    name: Final = "Colour Flash"
    required_edgework: Final = ()

    def stage(self) -> None:
        pass
