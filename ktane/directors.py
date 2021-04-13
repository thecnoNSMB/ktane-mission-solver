"Contains coordinating structure and utility for bomb management and solvers."

from collections import deque
from enum import Enum, Flag, auto
from typing import Deque, Tuple, Optional, Final
from abc import ABC, abstractmethod

from ktane.ask import talk
from ktane import ask

__all__ = ["EdgeFlag", "Edgework", "ModuleSolver", "BombSolver"]

IndicatorList = Tuple[Tuple[str, bool], ...]
PortPlateList = Tuple[Tuple['Port', ...], ...]

#resolve conflicts where mypy and pylint both report the same issue, as needed

class Port(Enum):
    "Ports for edgework information."
    DVID = auto()
    PARALLEL = auto()
    PS2 = auto()
    RJ45 = auto()
    SERIAL = auto()
    RCA = auto()

class EdgeFlag(Flag):
    "Bitwise flags for edgework requirements."
    NONE = 0
    START_TIME_MINS = auto()
    MAX_STRIKES = auto()
    BATTERIES = auto()
    INDICATORS = auto()
    SERIAL = auto()
    PORTS = auto()
    TOTAL_MODULES = auto() #dummy flag for solvers, will always be initialized
    STRIKES = auto() #dummy flag for solvers, will always be initialized
    SOLVES = auto() #dummy flag for solvers, will always be initialized

class Edgework: #pylint: disable=too-many-instance-attributes #can't help it
    "Data object containing edgework information and bomb metadata."

    def __init__(self) -> None:
        self.start_time_mins: int = -1
        self.total_modules: int = 0
        self.max_strikes: int = -1
        self.batteries: int = 0
        self.indicators: IndicatorList = ()
        self.serial: str = ''
        self.port_plates: PortPlateList = ()
        self.strikes: int = 0
        self.solves: int = 0

        self._required_edgework_flag: EdgeFlag = EdgeFlag.NONE

    def set_edgeflags(self, flags: Tuple[EdgeFlag, ...]) -> None:
        "Mark that the given kinds of edgework are needed for this bomb."
        for flag in flags:
            self._required_edgework_flag |= flag

    def post_init(self, *, #pylint: disable=too-many-arguments #can't help it
                  start_time_mins: Optional[int] = None,
                  total_modules: Optional[int] = None,
                  max_strikes: Optional[int] = None,
                  batteries: Optional[int] = None,
                  indicators: Optional[IndicatorList] = None,
                  serial: Optional[str] = None,
                  port_plates: Optional[PortPlateList] = None,
                  strikes: Optional[int] = None,
                  solves: Optional[int] = None,
                  ) -> None:
        "Set all the fields, and ask the user to supply the readout if needed."
        self._get_start_time_mins(start_time_mins)
        self._get_total_modules(total_modules)
        self._get_max_strikes(max_strikes)
        self._get_batteries(batteries)
        self._get_indicators(indicators)
        self._get_serial(serial)
        self._get_ports(port_plates)
        self._get_strikes(strikes)
        self._get_solves(solves)

    #region private helper methods

    _port_names: Final = {"dvid", "parallel", "ps2", "rj45", "serial", "rca"}
    _port_name_to_enum: Final = {
        "dvid": Port.DVID, "parallel": Port.PARALLEL, "ps2": Port.PS2,
        "rj45": Port.RJ45, "serial": Port.SERIAL, "rca": Port.RCA
    }

    def _get_start_time_mins(self, start_time_mins: Optional[int]) -> None:
        if start_time_mins is not None and start_time_mins > 0:
            self.start_time_mins = start_time_mins
        elif EdgeFlag.START_TIME_MINS in self._required_edgework_flag:
            talk("What is the starting time on the bomb, in minutes?")
            talk("(In Zen mode, this is the time the bomb was generated with.)")
            self.start_time_mins = ask.positive_int()

    def _get_max_strikes(self, max_strikes: Optional[int]) -> None:
        if max_strikes is not None and max_strikes > 0:
            self.max_strikes = max_strikes
        elif EdgeFlag.MAX_STRIKES in self._required_edgework_flag:
            talk("How many strikes will cause the bomb to detonate?")
            self.max_strikes = ask.positive_int()

    def _get_batteries(self, batteries: Optional[int]) -> None:
        if batteries is not None and batteries >= 0:
            self.batteries = batteries
        elif EdgeFlag.BATTERIES in self._required_edgework_flag:
            talk("How many batteries are on the bomb?")
            self.batteries = int(ask.str_from_regex(r'[0-9]+'))

    def _get_indicators(self, indicators: Optional[IndicatorList]) -> None:
        if indicators is not None:
            self.indicators = indicators
        elif EdgeFlag.INDICATORS in self._required_edgework_flag:
            if ask.yes_no("Are there any indicators?"):
                talk("Input each indicator, one per line.")
                talk('Lowercase means unlit and uppercase means lit,')
                talk('so "CAR" is a lit CAR, and "frk" is an unlit FRK.')
                indicator_list_raw = ask.list_from_regex(r'[a-z]{3}|[A-Z]{3}',
                                                         case_sensitive=True)
                self.indicators = tuple((ind.lower(), ind.isupper())
                                        for ind in indicator_list_raw)
            #otherwise, the default is no indicators and will do

    def _get_serial(self, serial: Optional[str]) -> None:
        if serial is not None and self._serial_valid(serial):
            self.serial = serial
        elif EdgeFlag.SERIAL in self._required_edgework_flag:
            talk("What is the serial number?")
            self.serial = ask.str_from_func(self._serial_valid).lower()

    def _serial_valid(self, serial: str) -> bool:
        "Check if a potential serial number is valid."
        return (serial.isalnum() and len(serial) == 6
                and not (serial.isalpha() or serial.isdigit()))

    def _get_ports(self, port_plates: Optional[PortPlateList]) -> None:
        if port_plates is not None:
            self.port_plates = port_plates
        elif EdgeFlag.PORTS in self._required_edgework_flag:
            if ask.yes_no("Are there any port plates?"):
                talk("How many port plates are there?")
                plate_count = ask.positive_int()
                for i in range(plate_count):
                    talk(f"What ports, if any, are on plate {i+1}?")
                    plate = ask.list_from_set(self._port_names, print_options=True,)
                    #dirty tuple hacking
                    #todo: fix the dirty tuple hacking?
                    self.port_plates = (*self.port_plates,
                                        tuple(self._port_name_to_enum[port]
                                              for port in plate))
            #otherwise, the default is no plates and will do

    def _get_total_modules(self, total_modules: Optional[int]) -> None:
        if total_modules is not None:
            if total_modules < 0:
                total_modules = 0
            self.total_modules = total_modules

    def _get_strikes(self, strikes: Optional[int]) -> None:
        if strikes is not None:
            if strikes < 0:
                strikes = 0
            elif self.max_strikes != -1 and strikes > self.max_strikes:
                strikes = self.max_strikes
            self.strikes = strikes

    def _get_solves(self, solves: Optional[int]) -> None:
        if solves is not None:
            if solves < 0:
                solves = 0
            elif solves > self.total_modules:
                solves = self.total_modules
            self.solves = solves

    #endregion

    def add_strike(self) -> None:
        "Add a strike, and quit if we hit the strike limit."
        self.strikes += 1
        if self.hit_strike_limit:
            talk("Bomb exploded! Hopefully it wasn't my fault.")
            raise SystemExit

    def add_solve(self) -> None:
        "Add a solve."
        self.solves += 1

    @property
    def hit_strike_limit(self) -> bool:
        "Whether the bomb has hit or breached the strike limit."
        if self.max_strikes != -1:
            return self.strikes >= self.max_strikes
        return False

    @property
    def defused(self) -> bool:
        "Whether the bomb has been defused (all present modules are solved)."
        return self.solves >= self.total_modules

    @property
    def serial_odd(self) -> bool:
        "Whether or not the last digit of the serial number is odd."
        if self.serial:
            return bool([int(c) for c in self.serial if c.isdigit()][-1] % 2)
        return False #undefined behavior

    @property
    def serial_vowel(self) -> bool:
        "Whether or not the serial number contains a vowel."
        if self.serial:
            return any(v in self.serial for v in 'aeiou')
        return False

    def has_port(self, port: Port) -> bool:
        "Whether or not the bomb has the given port."
        return any(port in plate for plate in self.port_plates)

class ModuleSolver(ABC):
    "Prototype class for regular module solvers."
    bomb: Edgework #Should be assigned directly by managing BombSolver
    bomb_solver: 'BombSolver' #Same as above

    #The following may be defined statically by subclasses as needed:
    total_stages: int = 1
    reset_stages_on_strike: bool = False

    @property
    @abstractmethod
    def name(self) -> str:
        "The name of the module."

    @property
    @abstractmethod
    def required_edgework(self) -> Tuple[EdgeFlag, ...]:
        "Flags indicating the edgework this module needs to know."

    def custom_data_init(self) -> None:
        "Initializer routine for solver-specific data. May be overridden."

    def custom_data_clear(self) -> None:
        """Destructor routine for solver-specific data.
        Should be overridden if custom_data_init is overridden."""

    @abstractmethod
    def stage(self) -> None:
        "Solve a single stage (the entire module if unstaged)."

    #region: default handling

    def __init__(self, count: int = 1):
        self.total_count: Final[int] = count
        self.solved_count: int = 0
        self.current_stage: int = 0
        self.custom_data_init()

    def post_init(self, edgework: Edgework, bomb_solver: 'BombSolver') -> None:
        """Set the Edgework and BombSolver the module solver will use.
        Should be called before a solve is attempted."""
        self.bomb = edgework
        self.bomb_solver = bomb_solver
        self.bomb.set_edgeflags(self.required_edgework)

    def announce(self) -> None:
        """Print the Now Solving message for this module.
        To be used only at the start of each new module."""
        module_number = self.solved_count + 1
        talk(f"--- NOW SOLVING: {self.name} #{module_number}", warning_bypass=True)

    def do_stage(self) -> bool:
        "Set up the next stage, and return False if all stages are done."
        self.current_stage += 1
        stages_not_done = (self.current_stage <= self.total_stages)
        if self.total_stages > 1 and stages_not_done:
            talk(f"- STAGE {self.current_stage}")
        return stages_not_done

    def reset_stages(self) -> None:
        "Reset stage progress."
        self.current_stage = 0
        self.custom_data_clear()

    def solve(self) -> None:
        "Solve one instance of this module in its entirety."
        self.announce()
        while self.do_stage():
            self.stage()
            self.check_strike()
        if not self.check_solve():
            self.reset_stages() #undefined behavior

    def check_strike(self) -> None:
        "Ask whether a strike occurred, and handle it if so."
        if ask.yes_no("Did the module strike?"):
            self.bomb.add_strike()
            self.on_this_struck()
            self.bomb_solver.handle_strike()

    def check_solve(self) -> bool:
        """Ask whether a solve occurred, and handle it if so.
        Return True if a solve in fact occurred."""
        if ask.yes_no("Did the module solve?"):
            self.bomb.add_solve()
            self.on_this_solved()
            self.bomb_solver.handle_solve()
            return True
        return False

    def on_this_struck(self) -> None:
        "Handle when this module produces a strike."
        if self.reset_stages_on_strike:
            self.reset_stages()
        else:
            self.current_stage -= 1

    def on_this_solved(self) -> None:
        "Handle when this module produces a solve."
        self.reset_stages()
        self.solved_count += 1

    #endregion

    @property
    def all_solved(self) -> bool:
        "Whether all modules of this type are solved."
        return self.solved_count >= self.total_count

class BombSolver:
    """Object that handles bomb-scale tasks, like boss modules, strike and
    solve handling, and the solve queue. Does not contain any solvers."""
    edgework: Edgework
    queue: Deque[ModuleSolver] #for now this must contain every module
    #eventually it will be split into one for regular modules and one for bosses

    def __init__(self, *queue: ModuleSolver):
        self.queue = deque(queue)
        self.edgework = Edgework()
        self.initialize_solvers()

    def count_modules(self) -> int:
        """Determine how many individual modules are on the bomb.
        Should only be called before edgework initialization."""
        return sum(solver.total_count for solver in self.queue)

    def initialize_solvers(self) -> None:
        """Supply the correct edgework to all solvers in the queue,
        and other initialization tasks in future as needed."""
        for solver in self.queue:
            solver.post_init(self.edgework, self)

    def initialize_edgework(self, *, start_time_mins: Optional[int] = None,
                            max_strikes: Optional[int] = None) -> None:
        "Initialize the edgework object and acquire all edgework info."
        self.edgework.post_init(
            start_time_mins=start_time_mins,
            total_modules=self.count_modules(),
            max_strikes=max_strikes,
        )

    def handle_strike(self) -> None:
        "Do any processing that needs to be done after each strike."

    def handle_solve(self) -> None:
        "Do any processing that needs to be done after each solve."

    def resort_queue(self) -> None:
        """Pass the queue through every solver subscribed to this event
        to ensure that the solve queue is in an acceptable state."""

    def solve(self, *, start_time_mins: Optional[int] = None,
              max_strikes: Optional[int] = None) -> None:
        "Get edgework information, call each solver in turn, and do associated handling."
        self.initialize_edgework(start_time_mins=start_time_mins, max_strikes=max_strikes)
        while self.queue:
            if self.edgework.defused:
                raise RuntimeError("Bomb defused with items on the queue.")
            solver = self.queue.pop()
            solver.solve()
            if not solver.all_solved:
                self.queue.append(solver)
            self.resort_queue()
        if self.edgework.defused:
            talk("Bomb defused!")
        else:
            raise RuntimeError("Queue empty but bomb not defused.")
