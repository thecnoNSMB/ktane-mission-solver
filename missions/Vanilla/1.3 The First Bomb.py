from ktane.directors import BombSolver
from ktane.vanilla import Keypad, TheButton, Wires

BombSolver(Keypad(), TheButton(), Wires()).solve()
