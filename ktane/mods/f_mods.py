"""Modded modules whose names begin with the letter F."""

from string import ascii_lowercase
from typing import Final, List

from ktane import ask
from ktane.directors import EdgeFlag, ModuleSolver, Port

__all__ = [
    "FollowTheLeader",
]


class FollowTheLeader(ModuleSolver):
    """Solver for Follow the Leader."""

    name: Final = "Follow the Leader"
    id: Final = "FollowTheLeaderModule"
    required_edgework: Final = (
        EdgeFlag.PORTS, EdgeFlag.SERIAL, EdgeFlag.BATTERIES, EdgeFlag.INDICATORS,
    )

    valid_colors: Final = {"red", "yellow", "green", "blue", "black", "white"}

    def stage(self) -> None:
        ask.talk("What plugs are the wires connected to, in numeric order?")
        wire_plugs = ask.list_from_set(
            {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"},
        )
        ask.talk(
            "Starting from plug {0}, ".format(wire_plugs[0])
            + "what colors are the wires in clockwise order?",
        )
        wire_colors = ask.list_from_set(self.valid_colors, expected_len=len(wire_plugs))
        start_index: int
        if self.bomb.has_port(Port.RJ45) and ("4" in wire_plugs and "5" in wire_plugs):
            start_index = wire_plugs.index("4")
        elif str(self.bomb.batteries) in wire_plugs:
            start_index = wire_plugs.index(str(self.bomb.batteries))
        elif self.bomb.serial_first_digit in wire_plugs:
            start_index = wire_plugs.index(self.bomb.serial_first_digit)
        elif self.bomb.has_indicator("CLR", lit=True):
            ask.talk("Cut all of the wires in descending numeric order.")
            return
        else:
            start_index = 0
        self.wire_loop(wire_plugs, wire_colors, start_index)

    def wire_loop(
        self, wire_plugs: List[str], wire_colors: List[str], start_index: int,
    ) -> None:
        """Given a starting index, determine which wires in the loop to cut."""
        rules_reverse_order = wire_colors[start_index] in {"red", "green", "white"}
        rules_direction = -1 if rules_reverse_order else 1
        current_index = start_index
        current_plug = wire_plugs[current_index]
        prev_cut = True
        ask.talk("Cut the wire starting at plug {0}.".format(current_plug))

        prev_index = current_index
        prev_color = wire_colors[prev_index]
        current_index = (current_index + 1) % len(wire_plugs)
        num_rules = 13
        current_rule: int
        if self.bomb.serial_first_letter:
            current_rule = ascii_lowercase.index(
                self.bomb.serial_first_letter,
            ) % num_rules
        else:
            current_rule = 0
        while current_index != start_index:
            rules_table = (
                prev_color not in {"yellow", "blue", "green"},
                int(current_plug) % 2 == 0,
                prev_cut,
                prev_color in {"red", "blue", "black"},
                len({
                    wire_colors[index] for index in range(prev_index, prev_index - 3, -1)
                }) < 3,
                (
                    (prev_color == wire_colors[current_index])
                    != (wire_colors[prev_index - 1] == wire_colors[current_index])
                ),  # != is equivalent to xor in this context
                prev_color in {"yellow", "white", "green"},
                not prev_cut,
                int(wire_plugs[prev_index]) + 1 != int(current_plug),
                prev_color not in {"white", "black", "red"},
                prev_color != wire_colors[prev_index - 1],
                int(current_plug) > 6,
                (
                    prev_color not in {"white", "black"}
                    or wire_colors[prev_index - 1] not in {"white", "black"}
                ),
            )
            prev_cut = rules_table[current_rule]

            if prev_cut:
                ask.talk("Cut the wire starting at plug {0}.".format(current_plug))
            prev_index = current_index
            prev_color = wire_colors[prev_index]
            current_index = (current_index + 1) % len(wire_plugs)
            current_plug = wire_plugs[current_index]
            current_rule = (current_rule + rules_direction) % num_rules
