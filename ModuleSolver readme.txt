HOW TO MAKE A SOLVER

Make a class subclassing ModuleSolver. It must provide the following:
name: The name of the module for printing.
    Example: "Forget Me Not"
required_edgework: The edgework information this module needs to know.
    Example: (EdgeFlag.BATTERIES, EdgeFlag.SERIAL)
stage(): The method which is called to solve a single stage of the module,
    or the module in its entirety if it's unstaged (the default).

Other things it can provide:
total_stages: The total number of stages on the module.
    Default: 1
reset_stages_on_strike: Whether a strike starts the module over from stage 1.
    Default: False
custom_data_init(): Called automatically on object creation.
    Used to initialize module-specific custom data.
custom_data_clear(): Called automatically on module solve or stage reset.
    Used to clear module-specific custom data.

Other elements:
total_count: The total number of module instances.
solved_count: The number of instances of this module that are solved.
current_stage: The current stage number.
    Will always be correct within stage(), may be off by one elsewhere.
announce(): Prints the name and number of the module.
do_stage(): Sets up the next stage and returns False if all stages are done.
reset_stages(): Resets stage count.
solve(): Solves all stages of the module, checking for strikes and solve.
check_strike(): Checks for a strike, and handles it if there was one.
check_solve(): Checks for a solve, and handles it if there was one.
    Also returns True if there was a solve.
on_this_struck(): Handles when this module strikes.
on_this_solved(): Handles when this module solves.
all_solved: Whether all modules of this type are solved. Not for internal use.