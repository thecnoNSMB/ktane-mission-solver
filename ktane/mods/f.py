"Modded modules whose names begin with the letter F."

from typing import Final, List

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
        self.wire_loop(wire_plugs, wire_colors, start_index)

    def wire_loop(self, wire_plugs: List[str],  #pylint: disable=too-many-branches
                  wire_colors: List[str], start_index: int) -> None:
        "Given a starting index, determine which wires in the loop to cut."
        rules_reverse_order = wire_colors[start_index] in ('red', 'green', 'white')
        current_index = start_index
        prev_cut = True
        talk(f"Cut the wire starting at plug {current_index}.")

        prev_index = current_index
        current_index = (current_index + 1) % len(wire_plugs)
        current_rule: int
        if self.bomb.serial_first_letter:
            current_rule = "abcdefghijklmnopqrstuvwxyz".index(
                self.bomb.serial_first_letter) % 13
        else:
            current_rule = 0
        while current_index != start_index:
            if (current_rule == 0
                    and wire_colors[prev_index] not in {"yellow", "blue", "green"}):
                prev_cut = True
            elif current_rule == 1 and int(wire_plugs[prev_index]) % 2 == 0:
                prev_cut = True
            elif current_rule == 2 and prev_cut:
                prev_cut = True
            elif current_rule == 3 and True:
                prev_cut = True
            elif current_rule == 4 and True:
                prev_cut = True
            elif current_rule == 5 and True:
                prev_cut = True
            elif current_rule == 6 and True:
                prev_cut = True
            elif current_rule == 7 and not prev_cut:
                prev_cut = True
            elif current_rule == 8 and True:
                prev_cut = True
            elif current_rule == 9 and True:
                prev_cut = True
            elif current_rule == 10 and True:
                prev_cut = True
            elif current_rule == 11 and True:
                prev_cut = True
            elif current_rule == 12 and True:
                prev_cut = True
            else:
                prev_cut = False

            if prev_cut:
                talk(f"Cut the wire starting at plug {current_index}.")
            prev_index = current_index
            current_index = (current_index + 1) % len(wire_plugs)
            current_rule = (current_rule + (-1 if rules_reverse_order else 1)) % 13
