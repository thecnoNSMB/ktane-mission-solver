"Modded modules whose names begin with the letter T."

from typing import Final

from ktane.directors import ModuleSolver

#todo: turn the keys
class TurnTheKeys(ModuleSolver):
    "Solver for Turn The Keys."
    name: Final = "Turn The Keys"
    required_edgework: Final = ()

    def stage(self) -> None:
        pass
