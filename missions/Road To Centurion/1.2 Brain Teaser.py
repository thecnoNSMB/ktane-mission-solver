from ktane.directors import BombSolver, from_pool
from ktane.mods.c import ColourFlash
from ktane.vanilla import (ComplicatedWires, Memory, WhosOnFirst, WireSequence,
                           Password, Wires, TheButton, Keypad)

BombSolver(
    ColourFlash(),
    ComplicatedWires(),
    *from_pool(Memory, WhosOnFirst, WireSequence),
    *from_pool(Password, Wires, TheButton, Keypad)
).solve()
