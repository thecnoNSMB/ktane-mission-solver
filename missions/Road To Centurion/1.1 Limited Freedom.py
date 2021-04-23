from ktane.directors import BombSolver, from_pool
from ktane.module_pools import ALL_VANILLA
from ktane.mods.t import TurnTheKeys

BombSolver(
    TurnTheKeys(),
    *from_pool(*ALL_VANILLA, count=10)
).solve()
