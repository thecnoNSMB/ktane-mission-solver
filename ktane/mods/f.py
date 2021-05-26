"Modded modules whose names begin with the letter F."

from typing import Final

from ktane.directors import ModuleSolver, EdgeFlag, Port
from ktane.ask import talk
from ktane import ask

__all__ = [
    "FollowTheLeader",
]

class FollowTheLeader(ModuleSolver):
    "Solver for Follow the Leader."
    name: Final = "Follow the Leader"
    id: Final = "FollowTheLeaderModule"
    required_edgework: Final = (EdgeFlag.PORTS, EdgeFlag.SERIAL, EdgeFlag.BATTERIES,
                                EdgeFlag.INDICATORS)

    valid_colors: Final = {'red', 'yellow', 'green', 'blue', 'black', 'white'}

    def stage(self) -> None:
        talk("What plugs are the wires connected to?")
        wire_plugs = ask.list_from_set({'1', '2', '3', '4', '5', '6',
                                        '7', '8', '9', '10', '11', '12'})
        talk("The wires are connected in clockwise order.")
        talk("Starting from plug 1, what colors are the wires in order?")
        wires = ask.list_from_set(self.valid_colors, expected_len=len(wire_plugs))
        if self.bomb.has_port(Port.RJ45) and ('4' in wire_plugs and '5' in wire_plugs):
            pass
