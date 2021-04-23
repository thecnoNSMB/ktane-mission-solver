"Contains some useful default pools for mission solvers."

from typing import Final

from ktane import vanilla
from ktane.mods import t

ALL_VANILLA: Final = (
    vanilla.Wires,
    vanilla.TheButton,
    vanilla.Keypad,
    vanilla.SimonSays,
    vanilla.WhosOnFirst,
    vanilla.Memory,
    vanilla.MorseCode,
    vanilla.ComplicatedWires,
    vanilla.WireSequence,
    vanilla.Maze,
    vanilla.Password,
)

ALL_MODS: Final = (
    t.TurnTheKeys,
)

ALL_SOLVABLE: Final = ALL_VANILLA + ALL_MODS
