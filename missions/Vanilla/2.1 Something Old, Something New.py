from ktane.directors import BombSolver, from_pool
from ktane.vanilla import Keypad, TheButton, Wires, Memory, Maze, SimonSays

BombSolver(
    *from_pool(Keypad, TheButton, Wires, count=2),
    *from_pool(Memory, Maze, SimonSays)
).solve()
