from ktane.directors import BombSolver, modules_from_pool
from ktane.mods.c_mods import ColourFlash
from ktane.vanilla import *

BombSolver(
    ColourFlash(),
    ComplicatedWires(),
    *modules_from_pool(Memory, WhosOnFirst, WireSequence),
    *modules_from_pool(Password, Wires, TheButton, Keypad),
).solve()
