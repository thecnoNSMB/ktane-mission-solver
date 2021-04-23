from ktane.directors import BombSolver, from_pool
from ktane.vanilla import (Wires, TheButton, Keypad, SimonSays, WhosOnFirst, Memory,
                           MorseCode, ComplicatedWires, WireSequence, Maze, Password)
from ktane.mods.t import TurnTheKeys

BombSolver(
    TurnTheKeys(),
    *from_pool(Wires, TheButton, Keypad, SimonSays, WhosOnFirst, Memory, MorseCode,
               ComplicatedWires, WireSequence, Maze, Password, count=10)
).solve()
