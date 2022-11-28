# ktane-mission-solver
A Python 3.8 package that can easily guide you through defusing KTANE bombs you specify.

Currently only supports vanilla modules and a few modded modules. Support for more modded modules (and maybe needies) will be added in future. Its experting profile is `Ktane Mission Solver.json`, though it won't cooperate with other experts.

To use, import `BombSolver` from `ktane.directors`, supply it with `ModuleSolver` subclasses matching the modules on your bomb,
and call `solve()` on it (optionally specifying time and strike limits). See the mission scripts in missions for examples.
