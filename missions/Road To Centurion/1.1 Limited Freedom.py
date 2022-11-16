from ktane.directors import BombSolver, modules_from_pool
from ktane.mods.t_mods import TurnTheKeys
from ktane.module_pools import ALL_VANILLA

BombSolver(
    TurnTheKeys(),
    *modules_from_pool(*ALL_VANILLA, count=10),
).solve()
