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
        talk("What plugs are the wires connected to, in numeric order?")
        wire_plugs = ask.list_from_set({'1', '2', '3', '4', '5', '6',
                                        '7', '8', '9', '10', '11', '12'})
        talk("Starting from plug 1, what colors are the wires in clockwise order?")
        wire_colors = ask.list_from_set(self.valid_colors, expected_len=len(wire_plugs))
        wires = list(zip(wire_plugs, wire_colors))
        start_index: int
        if self.bomb.has_port(Port.RJ45) and ('4' in wire_plugs and '5' in wire_plugs):
            start_index = wire_plugs.index('4')
        elif str(self.bomb.batteries) in wire_plugs:
            start_index = wire_plugs.index(str(self.bomb.batteries))
        elif self.bomb.serial_first_digit in wire_plugs:
            start_index = wire_plugs.index(self.bomb.serial_first_digit)
        elif not self.bomb.has_indicator('CLR', True):
            start_index = 0
        else:
            talk("Cut all of the wires in reverse order.")
            return
        current_index = start_index
        talk(f"Cut the wire starting at plug {current_index}.")
        current_index = (current_index + 1) % len(wire_plugs)
        while current_index != start_index:
            current_index = (current_index + 1) % len(wire_plugs)
