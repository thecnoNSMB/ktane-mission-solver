from ktane.directors import BombSolver, modules_from_pool
from ktane.mods.f_mods import FollowTheLeader
from ktane.vanilla import ComplicatedWires, Wires, WireSequence

BombSolver(
    Wires(),
    ComplicatedWires(),
    WireSequence(),
    FollowTheLeader(),
    *modules_from_pool(Wires, ComplicatedWires),
).solve()
