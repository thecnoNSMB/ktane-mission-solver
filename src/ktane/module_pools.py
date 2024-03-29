"""Contains some useful default pools for mission solvers."""

from typing import Final

from ktane import mods, vanilla

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
    mods.a_mods.Anagrams,
    mods.c_mods.ColourFlash,
    mods.c_mods.CrazyTalk,
    mods.f_mods.FollowTheLeader,
    mods.t_mods.TurnTheKeys,
    mods.w_mods.WordScramble,
)

ALL_SOLVABLE: Final = ALL_VANILLA + ALL_MODS
