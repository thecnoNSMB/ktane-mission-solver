"""Modded modules whose names begin with the letter T."""

from collections import deque  # TurnTheKeys
from typing import Deque, Final

from ktane import ask
from ktane.directors import ModuleSolver

__all__ = [
    "TurnTheKeys",
]


class TurnTheKeys(ModuleSolver):
    """Solver for Turn The Keys."""

    name: Final = "Turn The Keys"
    id: Final = "TurnTheKeyAdvanced"
    required_edgework: Final = ()

    required_solves: Final = (
        # vanilla modules
        "BigButton",  # The Button
        "Keypad",
        "Morse",
        "Password",
        "WhosOnFirst",
        "Wires",
        # modded modules
        "ColourFlash",
        "CrazyTalk",
        "KeypadV2",  # Round Keypad
        "Listening",
        "OrientationCube",
        "TwoBits",
    )
    banned_solves: Final = (
        # vanilla modules
        "Maze",
        "Memory",
        "Simon",
        "Venn",  # Complicated Wires
        "WireSequence",
        # modded modules
        "combinationLock",
        "CryptModule",  # Cryptography
        "MazeV2",  # Plumbing
        "Semaphore",
        "spwizAstrology",  # Astrology
        "switchModule",  # Switches
    )

    right_keys_turned: bool

    def resort_queue(self, queue: Deque[ModuleSolver]) -> Deque[ModuleSolver]:
        # TODO: only resort if needed
        new_queue = deque(
            module for module in queue
            if module.id not in self.required_solves
            and module.id not in self.banned_solves
        )
        new_queue.extend(module for module in queue if module.id in self.required_solves)
        new_queue.extendleft(
            module for module in queue if module.id in self.banned_solves
        )
        return new_queue

    def custom_data_init(self) -> None:
        self.right_keys_turned: bool = False

    def on_this_solved(self) -> None:
        self.right_keys_turned = True
        super().on_this_solved()

    def stage(self) -> None:
        if not self.right_keys_turned:
            ask.talk(
                "This module and others like it have a"
                + " number displaying each module's priority.",
            )  # TODO: display first time this bomb only
            ask.talk(
                "Turn each right key on modules of this"
                + " type, in descending order of priority.",
            )
        ask.talk("Turn the lowest priority left key that hasn't already been turned.")
