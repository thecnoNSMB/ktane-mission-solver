"Modded modules whose names begin with the letter T."

from collections import deque #TurnTheKeys
from typing import Final, Deque

from ktane.directors import ModuleSolver
from ktane.ask import talk

__all__ = [
    "TurnTheKeys",
]

class TurnTheKeys(ModuleSolver):
    "Solver for Turn The Keys."
    name: Final = "Turn The Keys"
    id: Final = "TurnTheKeyAdvanced"
    required_edgework: Final = ()

    required_solves: Final = (
        "Password", "WhosOnFirst", "Keypad", "Morse", "Wires", "BigButton",
        "ColourFlash", #Crazy Talk, Listening, Orientation Cube, Two Bits, Round Keypad
    )
    banned_solves: Final = (
        "Maze", "Memory", "Venn", "WireSequence", "Simon",
        #Cryptography, Semaphore, Combination Lock, Astrology, Switches, Plumbing
    )

    right_keys_turned: bool

    def resort_queue(self, queue: Deque[ModuleSolver]) -> Deque[ModuleSolver]:
        #todo: only resort if needed
        new_queue = deque(module for module in queue
                          if module.id not in self.required_solves
                          and module.id not in self.banned_solves)
        new_queue.extend(module for module in queue
                         if module.id in self.required_solves)
        new_queue.extendleft(module for module in queue
                             if module.id in self.banned_solves)
        return new_queue

    def custom_data_init(self) -> None:
        self.right_keys_turned: bool = False

    def on_this_solved(self) -> None:
        self.right_keys_turned = True
        super().on_this_solved()

    def stage(self) -> None:
        if not self.right_keys_turned:
            talk("This module and others like it have a number"
                 " displaying each module's priority.") #first time this bomb only
            talk("Turn each right key on modules of this type,"
                 " in descending order of priority.")
        talk("Turn the lowest priority left key that hasn't already been turned.")
