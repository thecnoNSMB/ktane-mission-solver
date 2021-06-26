from ktane.directors import BombSolver, from_pool
from ktane.mods.f import FollowTheLeader
from ktane.vanilla import Wires, ComplicatedWires, WireSequence

BombSolver(
    Wires(),
    ComplicatedWires(),
    WireSequence(),
    FollowTheLeader(),
    *from_pool(Wires, ComplicatedWires)
).solve()
