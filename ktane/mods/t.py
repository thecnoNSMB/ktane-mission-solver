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
    required_edgework: Final = ()

    required_solves: Final = (
        "Password", "Who's on First", "Keypad", "Morse Code", "Wires", "The Button",
        #Crazy Talk, Listening, Orientation Cube, Two Bits, Colour Flash, Round Keypad
    )
    banned_solves: Final = (
        "Maze", "Memory", "Complicated Wires", "Wire Sequence", "Simon Says",
        #Cryptography, Semaphore, Combination Lock, Astrology, Switches, Plumbing
    )

    right_keys_turned: bool

    def resort_queue(self, queue: Deque[ModuleSolver]) -> Deque[ModuleSolver]:
        new_queue = deque(module for module in queue
                          if module.name not in self.required_solves
                          and module.name not in self.banned_solves)
        new_queue.extend(module for module in queue
                         if module.name in self.required_solves)
        new_queue.extendleft(module for module in queue
                             if module.name in self.banned_solves)
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
