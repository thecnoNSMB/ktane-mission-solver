"Modded modules whose names begin with the letter T."

from typing import Final

from ktane.directors import ModuleSolver
from ktane.ask import talk

#todo: turn the keys
class TurnTheKeys(ModuleSolver):
    "Solver for Turn The Keys."
    name: Final = "Turn The Keys"
    required_edgework: Final = ()

    right_keys_turned: bool

    def custom_data_init(self) -> None:
        self.right_keys_turned: bool = False

    def on_this_solved(self) -> None:
        self.right_keys_turned = True
        super().on_this_solved()

    def stage(self) -> None:
        talk("This module and others like it have a number"
             " displaying each module's priority.")
        if not self.right_keys_turned:
            talk("Turn each right key on modules of this type,"
                 " in descending order of priority.")
        talk("Turn the lowest priority left key that hasn't already been turned.")
