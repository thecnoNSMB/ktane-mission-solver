from ktane.directors import BombSolver, modules_from_pool
from ktane.vanilla import Keypad, Maze, Memory, SimonSays, TheButton, Wires

BombSolver(
    *modules_from_pool(Keypad, TheButton, Wires, count=2),
    *modules_from_pool(Memory, Maze, SimonSays),
).solve()
