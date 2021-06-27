"Contains some useful default pools for mission solvers."

from typing import Final

from ktane import vanilla, mods

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
    mods.a.Anagrams,
    mods.c.ColourFlash,
    mods.f.FollowTheLeader,
    mods.t.TurnTheKeys,
    mods.w.WordScramble,
)

ALL_SOLVABLE: Final = ALL_VANILLA + ALL_MODS
