"Modded modules whose names begin with the letter F."

from typing import Final

from ktane.directors import ModuleSolver, EdgeFlag

__all__ = [
    "FollowTheLeader",
]

class FollowTheLeader(ModuleSolver):
    "Solver for Follow the Leader."
    name: Final = "Follow the Leader"
    required_edgework: Final = (EdgeFlag.PORTS, EdgeFlag.SERIAL, EdgeFlag.BATTERIES,
                                EdgeFlag.INDICATORS)

    def stage(self) -> None:
        pass
