"""Solver scripts for all vanilla modules."""

from typing import Counter, Dict, Final, List, NamedTuple, Tuple

from ktane import ask
from ktane.directors import EdgeFlag, ModuleSolver, Port
from ktane.solverutils import grid, maze, morse  # MorseCode, Maze

__all__ = [
    "Wires",
    "TheButton",
    "Keypad",
    "SimonSays",
    "WhosOnFirst",
    "Memory",
    "MorseCode",
    "ComplicatedWires",
    "WireSequence",
    "Maze",
    "Password",
]


class Wires(ModuleSolver):
    """Solver for vanilla Wires."""

    name: Final = "Wires"
    id: Final = "Wires"
    required_edgework: Final = (EdgeFlag.SERIAL,)

    def stage(self) -> None:
        ask.talk("What color wires are on the module, from top to bottom?")
        ask.talk(
            "Type R for red, Y for yellow, B for blue, W for white, and K for black.",
        )
        wirelist = ask.str_from_regex(r"[rybwk]{3,6}").lower()
        wire: str
        if len(wirelist) == 3:
            if "r" not in wirelist:
                wire = "second"
            elif wirelist[-1] == "w":
                wire = "last"
            elif wirelist.count("b") > 1:
                wire = "last blue"
            else:
                wire = "last"
        elif len(wirelist) == 4:
            if wirelist.count("r") > 1 and self.bomb.serial_odd:
                wire = "last red"
            elif wirelist[-1] == "y" and "r" not in wirelist:
                wire = "first"
            elif wirelist.count("b") == 1:
                wire = "first"
            elif wirelist.count("y") > 1:
                wire = "last"
            else:
                wire = "second"
        elif len(wirelist) == 5:
            if wirelist[-1] == "k" and self.bomb.serial_odd:
                wire = "fourth"
            elif wirelist.count("r") == 1 and wirelist.count("y") > 1:
                wire = "first"
            elif "k" not in wirelist:
                wire = "second"
            else:
                wire = "first"
        elif len(wirelist) == 6:
            if "y" not in wirelist and self.bomb.serial_odd:
                wire = "third"
            elif wirelist.count("y") == 1 and wirelist.count("w") > 1:
                wire = "fourth"
            elif "r" not in wirelist:
                wire = "last"
            else:
                wire = "fourth"
        ask.talk("Cut the {location} wire.".format(location=wire))


class TheButton(ModuleSolver):
    """Solver for vanilla The Button."""

    name: Final = "The Button"
    id: Final = "BigButton"
    required_edgework: Final = (EdgeFlag.BATTERIES, EdgeFlag.INDICATORS)

    valid_colors: Final = {"red", "yellow", "blue", "white"}
    valid_labels: Final = {"abort", "detonate", "hold", "press"}

    def stage(self) -> None:
        ask.talk("What color is the button?")
        ask.talk('Type one of "red", "yellow", "blue", or "white", without quotes.')
        color = ask.str_from_set(self.valid_colors)
        ask.talk("What is the text on the label?")
        ask.talk('Type one of "abort", "detonate", "hold", or "press", without quotes.')
        label = ask.str_from_set(self.valid_labels)
        if color == "blue" and label == "abort":
            self._hold()
        elif self.bomb.batteries > 1 and label == "detonate":
            ask.talk("Press and immediately release the button.")
        elif color == "white" and ("car", True) in self.bomb.indicators:
            self._hold()
        elif self.bomb.batteries > 2 and ("frk", True) in self.bomb.indicators:
            ask.talk("Press and immediately release the button.")
        elif color == "yellow":
            self._hold()
        elif color == "red" and label == "hold":
            ask.talk("Press and immediately release the button.")
        else:
            self._hold()

    def _hold(self) -> None:
        ask.talk("Hold down the button. What color is the strip on the right?")
        ask.talk('Type one of "red", "yellow", "blue", or "white", without quotes.')
        strip = ask.str_from_set(self.valid_colors)
        digit: int
        if strip == "blue":
            digit = 4
        elif strip == "yellow":
            digit = 5
        else:
            digit = 1
        ask.talk(
            "Release the button when the countdown timer "
            + "has a {0} in any position.".format(digit),
        )


class Keypad(ModuleSolver):
    """Solver for vanilla Keypad."""

    name: Final = "Keypad"
    id: Final = "Keypad"
    required_edgework: Final = ()

    valid_symbols: Final = {
        "copyright",
        "filled star",
        "hollow star",
        "smiley face",
        "double k",
        "omega",
        "squidknife",
        "pumpkin",
        "hook n",
        "six",
        "squiggly n",
        "at",
        "ae",
        "melted three",
        "euro",
        "n with hat",
        "dragon",
        "question mark",
        "paragraph",
        "right c",
        "left c",
        "pitchfork",
        "cursive",
        "tracks",
        "balloon",
        "upside down y",
        "bt",
    }
    columns: Final = {  # TODO: type hint this?
        (
            "balloon",
            "at",
            "upside down y",
            "squiggly n",
            "squidknife",
            "hook n",
            "left c",
        ),
        (
            "euro",
            "balloon",
            "left c",
            "cursive",
            "hollow star",
            "hook n",
            "question mark",
        ),
        (
            "copyright",
            "pumpkin",
            "cursive",
            "double k",
            "melted three",
            "upside down y",
            "hollow star",
        ),
        (
            "six",
            "paragraph",
            "bt",
            "squidknife",
            "double k",
            "question mark",
            "smiley face",
        ),
        (
            "pitchfork",
            "smiley face",
            "bt",
            "right c",
            "paragraph",
            "dragon",
            "filled star",
        ),
        (
            "six",
            "euro",
            "tracks",
            "ae",
            "pitchfork",
            "n with hat",
            "omega",
        ),
    }

    def stage(self) -> None:
        ask.talk("What symbols are on the keypad?")
        symbols = ask.list_from_set(
            self.valid_symbols, print_options=True, expected_len=4,
        )
        while all(any(sym not in col for sym in symbols) for col in self.columns):
            ask.talk("I couldn't find a solution for those symbols.")
            ask.talk("Please ensure you typed them correctly.")
            ask.talk("What symbols are on the keypad?")
            symbols = ask.list_from_set(
                self.valid_symbols, print_options=True, expected_len=4,
            )
        for column in self.columns:
            if all(sym in column for sym in symbols):
                ask.talk("Press the keys in the following order:")
                for symbol in column:
                    if symbol in symbols:
                        ask.talk(symbol.upper())


class SimonSays(ModuleSolver):
    """Solver for vanilla Simon Says."""

    name: Final = "Simon Says"
    id: Final = "Simon"
    required_edgework: Final = (EdgeFlag.SERIAL, EdgeFlag.STRIKES)
    total_stages = 5  # max number of stages

    valid_colors: Final = {"red", "blue", "green", "yellow"}
    color_sequence: List[str]

    def stage(self) -> None:
        if self.current_stage == 1:
            ask.talk("What color is flashing?")
        else:
            ask.talk("What color is now flashing at the end of the sequence?")
        ask.talk('Type one of "red", "blue", "green", or "yellow", without quotes.')
        new_color = ask.str_from_set(self.valid_colors)
        self.color_sequence.append(new_color)
        if self.bomb.serial_vowel:
            if self.bomb.strikes == 0:
                simon_key = {
                    "red": "Blue", "blue": "Red", "green": "Yellow", "yellow": "Green",
                }
            elif self.bomb.strikes == 1:
                simon_key = {
                    "red": "Yellow", "blue": "Green", "green": "Blue", "yellow": "Red",
                }
            else:
                simon_key = {
                    "red": "Green", "blue": "Red", "green": "Yellow", "yellow": "Blue",
                }
        else:
            if self.bomb.strikes == 0:
                simon_key = {
                    "red": "Blue", "blue": "Yellow", "green": "Green", "yellow": "Red",
                }
            elif self.bomb.strikes == 1:
                simon_key = {
                    "red": "Red", "blue": "Blue", "green": "Yellow", "yellow": "Green",
                }
            else:
                simon_key = {
                    "red": "Yellow", "blue": "Green", "green": "Blue", "yellow": "Red",
                }
        ask.talk("Press the following colors in order:")
        for color in self.color_sequence:
            ask.talk(simon_key[color])

    def custom_data_init(self) -> None:
        self.color_sequence = []

    def custom_data_clear(self) -> None:
        self.color_sequence = []

    def solve(self) -> None:
        self.announce()
        while self.do_stage():
            self.stage()
            self.check_strike()
            if self.current_stage >= 3:
                if self.check_solve():
                    return
        self.reset_stages()

    def on_this_struck(self) -> None:
        super().on_this_struck()
        self.color_sequence.pop()


class WhosOnFirst(ModuleSolver):
    """Solver for vanilla Who's On First."""

    name: Final = "Who's on First"
    id: Final = "WhosOnFirst"
    required_edgework: Final = ()
    total_stages = 3

    valid_displays: Final = {
        "yes",
        "first",
        "display",
        "okay",
        "says",
        "nothing",
        "empty",
        "blank",
        "no",
        "led",
        "lead",
        "read",
        "red",
        "reed",
        "leed",
        "hold on",
        "you",
        "you are",
        "your",
        "you're",
        "ur",
        "there",
        "they're",
        "their",
        "they are",
        "see",
        "c",
        "cee",
    }
    valid_labels: Final = {
        "ready",
        "first",
        "no",
        "blank",
        "nothing",
        "yes",
        "what",
        "uhhh",
        "left",
        "right",
        "middle",
        "okay",
        "wait",
        "press",
        "you",
        "you are",
        "your",
        "you're",
        "ur",
        "u",
        "uh huh",
        "uh uh",
        "what?",
        "done",
        "next",
        "hold",
        "sure",
        "like",
    }
    display_to_index: Final = {
        "yes": 2,
        "first": 1,
        "display": 5,
        "okay": 1,
        "says": 5,
        "nothing": 2,
        "empty": 4,  # no text on display
        "blank": 3,
        "no": 5,
        "led": 2,
        "lead": 5,
        "read": 3,
        "red": 3,
        "reed": 4,
        "leed": 4,
        "hold on": 5,
        "you": 3,
        "you are": 5,
        "your": 3,
        "you're": 3,
        "ur": 0,
        "there": 5,
        "they're": 4,
        "their": 3,
        "they are": 2,
        "see": 5,
        "c": 1,
        "cee": 5,
    }
    label_to_buttons: Final = {
        "ready": ("yes", "okay", "what", "middle", "left", "press", "right", "blank"),
        "first": (
            "left",
            "okay",
            "yes",
            "middle",
            "no",
            "right",
            "nothing",
            "uhhh",
            "wait",
            "ready",
            "blank",
            "what",
            "press",
        ),
        "no": (
            "blank",
            "uhhh",
            "wait",
            "first",
            "what",
            "ready",
            "right",
            "yes",
            "nothing",
            "left",
            "press",
            "okay",
        ),
        "blank": ("wait", "right", "okay", "middle"),
        "nothing": (
            "uhhh",
            "right",
            "okay",
            "middle",
            "yes",
            "blank",
            "no",
            "press",
            "left",
            "what",
            "wait",
            "first",
        ),
        "yes": (
            "okay",
            "right",
            "uhhh",
            "middle",
            "first",
            "what",
            "press",
            "ready",
            "nothing",
        ),
        "what": ("uhhh",),
        "uhhh": (
            "ready",
            "nothing",
            "left",
            "what",
            "okay",
            "yes",
            "right",
            "no",
            "press",
            "blank",
        ),
        "left": ("right",),
        "right": ("yes", "nothing", "ready", "press", "no", "wait", "what"),
        "middle": (
            "blank", "ready", "okay", "what", "nothing", "press", "no", "wait", "left",
        ),
        "okay": ("middle", "no", "first", "yes", "uhhh", "nothing", "wait"),
        "wait": ("uhhh", "no", "blank", "okay", "yes", "left", "first", "press", "what"),
        "press": ("right", "middle", "yes", "ready"),
        "you": (
            "sure", "you are", "your", "you're", "next", "uh huh", "ur", "hold", "what?",
        ),
        "you are": (
            "your",
            "next",
            "like",
            "uh huh",
            "what?",
            "done",
            "uh uh",
            "hold",
            "you",
            "u",
            "you're",
            "sure",
            "ur",
        ),
        "your": ("uh uh", "you are", "uh huh"),
        "you're": ("you",),
        "ur": ("done", "u"),
        "u": ("uh huh", "sure", "next", "what?", "you're", "ur", "uh uh", "done"),
        "uh huh": (),
        "uh uh": ("ur", "u", "you are", "you're", "next"),
        "what?": (
            "you",
            "hold",
            "you're",
            "your",
            "u",
            "done",
            "uh uh",
            "like",
            "you are",
            "uh huh",
            "ur",
            "next",
        ),
        "done": (
            "sure",
            "uh huh",
            "next",
            "what?",
            "your",
            "ur",
            "you're",
            "hold",
            "like",
            "you",
            "u",
            "you are",
            "uh uh",
        ),
        "next": ("what?", "uh huh", "uh uh", "your", "hold", "sure"),
        "hold": (
            "you are",
            "u",
            "done",
            "uh uh",
            "you",
            "ur",
            "sure",
            "what?",
            "you're",
            "next",
        ),
        "sure": ("you are", "done", "like", "you're", "you", "hold", "uh huh", "ur"),
        "like": (
            "you're",
            "next",
            "u",
            "ur",
            "hold",
            "done",
            "uh uh",
            "what?",
            "uh huh",
            "you",
        ),
    }

    def stage(self) -> None:
        ask.talk('What text is on the display? (If there is no text, type "Empty".)')
        display = ask.str_from_set(self.valid_displays)
        ask.talk("What are the button labels, in reading order?")
        labels = ask.list_from_set(self.valid_labels, expected_len=6)
        label_index = self.display_to_index[display]
        key_label = labels[label_index]
        answer_label = key_label
        for button in self.label_to_buttons[key_label]:
            if button in labels:
                answer_label = button
                break
        ask.talk("Press the button labeled {0}.".format(answer_label.upper()))


class _MemoryStage(NamedTuple):
    label: str
    position: int


class Memory(ModuleSolver):
    """Solver for vanilla Memory."""

    name: Final = "Memory"
    id: Final = "Memory"
    required_edgework: Final = ()
    total_stages = 5
    reset_stages_on_strike = True

    presses: List[_MemoryStage]

    def custom_data_init(self) -> None:
        self.presses = []

    def custom_data_clear(self) -> None:
        self.presses = []

    def stage(self) -> None:
        ask.talk("What number is on the display?")
        display = int(ask.str_from_regex(r"[1-4]"))
        ask.talk("What numbers are on the buttons, in reading order?")
        buttons = ask.str_from_regex(r"[1-4]{4}")
        while any(char not in buttons for char in "1234"):
            ask.talk("There should be one of each number on the buttons.")
            ask.talk("What numbers are on the buttons, in reading order?")
            buttons = ask.str_from_regex(r"[1-4]{4}")
        stage: _MemoryStage
        if self.current_stage == 1:
            stage = self._stage_1(display, buttons)
        elif self.current_stage == 2:
            stage = self._stage_2(display, buttons)
        elif self.current_stage == 3:
            stage = self._stage_3(display, buttons)
        elif self.current_stage == 4:
            stage = self._stage_4(display, buttons)
        else:  # self.current_stage == 5
            stage = self._stage_5(display, buttons)
        ask.talk("Press the button labeled {0}.".format(stage.label))
        self.presses.append(stage)

    def _in_position(self, position: int, buttons: str) -> _MemoryStage:
        return _MemoryStage(buttons[position - 1], position)

    def _with_label(self, label: str, buttons: str) -> _MemoryStage:
        return _MemoryStage(label, buttons.index(label) + 1)

    def _stage_1(self, display: int, buttons: str) -> _MemoryStage:
        if display in {1, 2}:
            return self._in_position(2, buttons)
        if display == 3:
            return self._in_position(3, buttons)
        # display is 4
        return self._in_position(4, buttons)

    def _stage_2(self, display: int, buttons: str) -> _MemoryStage:
        if display == 1:
            return self._with_label("4", buttons)
        if display in {2, 4}:
            return self._in_position(self.presses[0].position, buttons)
        # display is 3
        return self._in_position(1, buttons)

    def _stage_3(self, display: int, buttons: str) -> _MemoryStage:
        if display == 1:
            return self._with_label(self.presses[1].label, buttons)
        if display == 2:
            return self._with_label(self.presses[0].label, buttons)
        if display == 3:
            return self._in_position(3, buttons)
        # display is 4
        return self._with_label("4", buttons)

    def _stage_4(self, display: int, buttons: str) -> _MemoryStage:
        if display == 1:
            return self._in_position(self.presses[0].position, buttons)
        if display == 2:
            return self._in_position(1, buttons)
        # display is 3 or 4
        return self._in_position(self.presses[1].position, buttons)

    def _stage_5(self, display: int, buttons: str) -> _MemoryStage:
        if display == 1:
            return self._with_label(self.presses[0].label, buttons)
        if display == 2:
            return self._with_label(self.presses[1].label, buttons)
        if display == 3:
            return self._with_label(self.presses[3].label, buttons)
        # display is 4
        return self._with_label(self.presses[2].label, buttons)


class MorseCode(ModuleSolver):
    """Solver for vanilla Morse Code."""

    name: Final = "Morse Code"
    id: Final = "Morse"
    required_edgework: Final = ()

    word_to_freq: Final = {
        "shell": "505",
        "halls": "515",
        "slick": "522",
        "trick": "532",
        "boxes": "535",
        "leaks": "542",
        "strobe": "545",
        "bistro": "552",
        "flick": "555",
        "bombs": "565",
        "break": "572",
        "brick": "575",
        "steak": "582",
        "sting": "592",
        "vector": "595",
        "beats": "600",
    }

    def stage(self) -> None:
        ask.talk("What Morse Code sequence is flashing?")
        word = morse.ask_word()
        while word not in self.word_to_freq:
            ask.talk("That word isn't in my table.")
            ask.talk("What Morse Code sequence is flashing?")
            word = morse.ask_word()
        ask.talk("Respond at frequency 3.{0} MHz.".format(self.word_to_freq[word]))


class ComplicatedWires(ModuleSolver):
    """Solver for vanilla Complicated Wires."""

    name: Final = "Complicated Wires"
    id: Final = "Venn"
    required_edgework: Final = (EdgeFlag.SERIAL, EdgeFlag.PORTS, EdgeFlag.BATTERIES)

    venn_diagram: Final = (
        # no red
        (
            # no blue
            #  none    L        S     SL
            ((("C"), ("D")), (("C"), ("B"))),
            # blue
            #  none    L        S     SL
            ((("S"), ("P")), (("D"), ("P"))),
        ),
        # red
        (
            # no blue
            #  none    L        S     SL
            ((("S"), ("B")), (("C"), ("B"))),
            # blue
            #  none    L        S     SL
            ((("S"), ("S")), (("P"), ("D"))),
        ),
    )

    def stage(self) -> None:
        ask.talk("What wires are on the module?")
        ask.talk("For each wire, include its colors, any of (R)ed, (B)lue, or (W)hite,")
        ask.talk("whether the LED above it is (L)it, and whether a (S)tar is present.")
        ask.talk("Input each wire as a string of the parenthesized letters above.")
        wirelist = ask.list_from_regex(r"[rbwls]+")
        for wire in wirelist:
            if self.cut(wire):
                ask.talk("Cut wire {0}.".format(wire.upper()))
            else:
                ask.talk("Do not cut wire {0}.".format(wire.upper()))

    def cut(self, wire: str) -> bool:
        """Determine whether a given wire must be cut."""
        action = self.venn_diagram["r" in wire]["b" in wire]["s" in wire]["l" in wire]
        if action == "C":
            return True
        if action == "D":
            return False
        if action == "S":
            return not self.bomb.serial_odd
        if action == "P":
            return self.bomb.has_port(Port.PARALLEL)
        if action == "B":
            return self.bomb.batteries >= 2
        raise RuntimeError("Invalid Venn Diagram action letter")


class _SequenceWire(NamedTuple):
    color: str
    label: str


class WireSequence(ModuleSolver):
    """Solver for vanilla Wire Sequence."""

    name: Final = "Wire Sequence"
    id: Final = "WireSequence"
    required_edgework: Final = ()
    total_stages = 4

    cut_table: Final[Dict[str, Tuple[str, ...]]] = {
        "red": ("c", "b", "a", "ac", "b", "ac", "abc", "ab", "b"),
        "blue": ("b", "ac", "b", "a", "b", "bc", "c", "ac", "a"),
        "black": ("abc", "ac", "b", "ac", "b", "bc", "ab", "c", "c"),
    }

    wire_counts: Counter[str]
    last_stage_counts: Counter[str]

    def custom_data_init(self) -> None:
        self.wire_counts = Counter()
        self.last_stage_counts = Counter()

    def custom_data_clear(self) -> None:
        self.wire_counts.clear()
        self.last_stage_counts.clear()

    def on_this_struck(self) -> None:
        self.last_stage_counts.clear()

    def ask_wires(self) -> Tuple[_SequenceWire, ...]:
        """Get a set of wires from the user."""
        ask.talk("What wires are on the panel, in order by their left plug?")
        ask.talk("Input their color followed by the letter")
        ask.talk('they\'re plugged into, like "red C".')
        wirelist = ask.list_from_func(self._check_wire_text)
        return tuple(_SequenceWire(*wire.split()) for wire in wirelist)

    def stage(self) -> None:
        # canonize last_stage_counts before starting new stage
        self.wire_counts.update(self.last_stage_counts)
        self.last_stage_counts.clear()
        wires = self.ask_wires()
        for wire in wires:
            self.last_stage_counts[wire.color] += 1
            wire_count = self.wire_counts[wire.color] + self.last_stage_counts[wire.color]
            if wire.label in self.cut_table[wire.color][wire_count - 1]:
                ask.talk(
                    "Cut the {0} wire connected to label {1}.".format(
                        wire.color, wire.label.upper(),
                    ),
                )
            else:
                ask.talk(
                    "Do not cut the {0} wire connected to label {1}.".format(
                        wire.color, wire.label.upper(),
                    ),
                )
        ask.talk("Press the down arrow to finish this panel.")

    @classmethod
    def _check_wire_text(cls, text: str) -> bool:
        if len(text.split()) != 2:
            return False
        if text.split()[0] not in cls.cut_table:
            return False
        return text.split()[1] in "abc"


class Maze(ModuleSolver):
    """Solver for vanilla Maze."""

    name: Final = "Maze"
    id: Final = "Maze"
    required_edgework: Final = ()

    mazes: Final[Tuple[Tuple[maze.Wall, ...], ...]] = (
        (
            maze.Wall(0, 5),
            maze.Wall(1, 2),
            maze.Wall(1, 8),
            maze.Wall(1, 10),
            maze.Wall(2, 1),
            maze.Wall(2, 5),
            maze.Wall(3, 4),
            maze.Wall(3, 6),
            maze.Wall(3, 8),
            maze.Wall(4, 1),
            maze.Wall(4, 5),
            maze.Wall(5, 2),
            maze.Wall(5, 8),
            maze.Wall(6, 1),
            maze.Wall(6, 7),
            maze.Wall(7, 2),
            maze.Wall(7, 4),
            maze.Wall(7, 6),
            maze.Wall(7, 8),
            maze.Wall(8, 5),
            maze.Wall(8, 9),
            maze.Wall(9, 2),
            maze.Wall(9, 8),
            maze.Wall(10, 3),
            maze.Wall(10, 7),
        ),
        (
            maze.Wall(0, 5),
            maze.Wall(1, 0),
            maze.Wall(1, 4),
            maze.Wall(1, 10),
            maze.Wall(2, 3),
            maze.Wall(2, 7),
            maze.Wall(3, 2),
            maze.Wall(3, 6),
            maze.Wall(3, 8),
            maze.Wall(4, 1),
            maze.Wall(4, 5),
            maze.Wall(5, 4),
            maze.Wall(5, 8),
            maze.Wall(6, 3),
            maze.Wall(6, 7),
            maze.Wall(6, 9),
            maze.Wall(7, 2),
            maze.Wall(7, 6),
            maze.Wall(8, 1),
            maze.Wall(8, 3),
            maze.Wall(8, 5),
            maze.Wall(8, 9),
            maze.Wall(9, 8),
            maze.Wall(10, 1),
            maze.Wall(10, 5),
        ),
        (
            maze.Wall(0, 5),
            maze.Wall(0, 7),
            maze.Wall(1, 2),
            maze.Wall(2, 1),
            maze.Wall(2, 3),
            maze.Wall(2, 5),
            maze.Wall(2, 9),
            maze.Wall(3, 0),
            maze.Wall(3, 6),
            maze.Wall(3, 8),
            maze.Wall(4, 3),
            maze.Wall(4, 5),
            maze.Wall(4, 9),
            maze.Wall(6, 1),
            maze.Wall(6, 3),
            maze.Wall(6, 5),
            maze.Wall(6, 7),
            maze.Wall(6, 9),
            maze.Wall(8, 1),
            maze.Wall(8, 5),
            maze.Wall(8, 7),
            maze.Wall(8, 9),
            maze.Wall(9, 2),
            maze.Wall(9, 4),
            maze.Wall(10, 7),
        ),
        (
            maze.Wall(0, 3),
            maze.Wall(1, 4),
            maze.Wall(1, 6),
            maze.Wall(1, 8),
            maze.Wall(2, 1),
            maze.Wall(2, 3),
            maze.Wall(3, 6),
            maze.Wall(3, 8),
            maze.Wall(4, 1),
            maze.Wall(4, 5),
            maze.Wall(4, 9),
            maze.Wall(5, 2),
            maze.Wall(5, 4),
            maze.Wall(5, 8),
            maze.Wall(6, 1),
            maze.Wall(7, 2),
            maze.Wall(7, 4),
            maze.Wall(7, 6),
            maze.Wall(7, 8),
            maze.Wall(8, 9),
            maze.Wall(9, 2),
            maze.Wall(9, 4),
            maze.Wall(9, 6),
            maze.Wall(10, 5),
            maze.Wall(10, 9),
        ),
        (
            maze.Wall(1, 0),
            maze.Wall(1, 2),
            maze.Wall(1, 4),
            maze.Wall(1, 6),
            maze.Wall(2, 9),
            maze.Wall(3, 2),
            maze.Wall(3, 4),
            maze.Wall(3, 8),
            maze.Wall(3, 10),
            maze.Wall(4, 3),
            maze.Wall(4, 7),
            maze.Wall(5, 4),
            maze.Wall(5, 6),
            maze.Wall(6, 1),
            maze.Wall(6, 7),
            maze.Wall(6, 9),
            maze.Wall(7, 2),
            maze.Wall(7, 4),
            maze.Wall(7, 8),
            maze.Wall(8, 1),
            maze.Wall(8, 9),
            maze.Wall(9, 4),
            maze.Wall(9, 6),
            maze.Wall(9, 8),
            maze.Wall(10, 1),
        ),
        (
            maze.Wall(0, 1),
            maze.Wall(0, 5),
            maze.Wall(1, 6),
            maze.Wall(2, 1),
            maze.Wall(2, 3),
            maze.Wall(2, 5),
            maze.Wall(2, 9),
            maze.Wall(3, 8),
            maze.Wall(4, 3),
            maze.Wall(4, 5),
            maze.Wall(4, 7),
            maze.Wall(5, 2),
            maze.Wall(5, 4),
            maze.Wall(5, 10),
            maze.Wall(6, 3),
            maze.Wall(6, 7),
            maze.Wall(6, 9),
            maze.Wall(7, 0),
            maze.Wall(8, 3),
            maze.Wall(8, 5),
            maze.Wall(8, 7),
            maze.Wall(9, 2),
            maze.Wall(9, 4),
            maze.Wall(9, 8),
            maze.Wall(10, 7),
        ),
        (
            maze.Wall(0, 7),
            maze.Wall(1, 2),
            maze.Wall(1, 4),
            maze.Wall(2, 1),
            maze.Wall(2, 5),
            maze.Wall(2, 9),
            maze.Wall(3, 4),
            maze.Wall(3, 6),
            maze.Wall(3, 8),
            maze.Wall(4, 3),
            maze.Wall(4, 7),
            maze.Wall(5, 0),
            maze.Wall(5, 2),
            maze.Wall(5, 6),
            maze.Wall(5, 10),
            maze.Wall(6, 3),
            maze.Wall(6, 9),
            maze.Wall(7, 6),
            maze.Wall(7, 8),
            maze.Wall(8, 1),
            maze.Wall(8, 3),
            maze.Wall(8, 9),
            maze.Wall(9, 2),
            maze.Wall(9, 4),
            maze.Wall(9, 6),
        ),
        (
            maze.Wall(0, 1),
            maze.Wall(0, 7),
            maze.Wall(1, 4),
            maze.Wall(2, 5),
            maze.Wall(2, 9),
            maze.Wall(3, 2),
            maze.Wall(3, 4),
            maze.Wall(3, 6),
            maze.Wall(3, 8),
            maze.Wall(4, 1),
            maze.Wall(4, 9),
            maze.Wall(5, 4),
            maze.Wall(5, 6),
            maze.Wall(6, 1),
            maze.Wall(6, 5),
            maze.Wall(7, 2),
            maze.Wall(7, 6),
            maze.Wall(7, 8),
            maze.Wall(7, 10),
            maze.Wall(8, 1),
            maze.Wall(8, 3),
            maze.Wall(9, 4),
            maze.Wall(9, 6),
            maze.Wall(9, 8),
            maze.Wall(9, 10),
        ),
        (
            maze.Wall(0, 1),
            maze.Wall(1, 4),
            maze.Wall(1, 6),
            maze.Wall(2, 1),
            maze.Wall(2, 3),
            maze.Wall(2, 7),
            maze.Wall(2, 9),
            maze.Wall(3, 6),
            maze.Wall(4, 5),
            maze.Wall(4, 9),
            maze.Wall(5, 2),
            maze.Wall(5, 4),
            maze.Wall(5, 8),
            maze.Wall(6, 1),
            maze.Wall(6, 3),
            maze.Wall(6, 7),
            maze.Wall(7, 6),
            maze.Wall(7, 8),
            maze.Wall(8, 1),
            maze.Wall(8, 3),
            maze.Wall(8, 5),
            maze.Wall(8, 9),
            maze.Wall(9, 10),
            maze.Wall(10, 3),
            maze.Wall(10, 7),
        ),
    )
    mark_to_maze: Dict[grid.Coord, Tuple[maze.Wall, ...]] = {
        grid.Coord(1, 0): mazes[0],
        grid.Coord(2, 5): mazes[0],
        grid.Coord(3, 1): mazes[1],
        grid.Coord(1, 4): mazes[1],
        grid.Coord(3, 3): mazes[2],
        grid.Coord(3, 5): mazes[2],
        grid.Coord(0, 0): mazes[3],
        grid.Coord(3, 0): mazes[3],
        grid.Coord(2, 4): mazes[4],
        grid.Coord(5, 3): mazes[4],
        grid.Coord(0, 4): mazes[5],
        grid.Coord(4, 2): mazes[5],
        grid.Coord(0, 1): mazes[6],
        grid.Coord(5, 1): mazes[6],
        grid.Coord(0, 3): mazes[7],
        grid.Coord(3, 2): mazes[7],
        grid.Coord(1, 2): mazes[8],
        grid.Coord(4, 0): mazes[8],
    }

    def stage(self) -> None:
        while True:
            ask.talk("What coordinate contains the white light?")
            start = maze.Node(*grid.ask_coord())
            ask.talk("What coordinate contains the red triangle?")
            goal = maze.Node(*grid.ask_coord())
            ask.talk("What coordinate contains a circular marking?")
            ask.talk("(You may use either one.)")
            marking = grid.ask_coord()
            while marking not in self.mark_to_maze:
                ask.talk("That doesn't fit any of the mazes.")
                ask.talk("What coordinate contains a circular marking?")
                ask.talk("(You may use either one.)")
                marking = grid.ask_coord()
            walls = self.mark_to_maze[marking]
            path = maze.solve_maze(grid.Dimensions(6, 6), start, goal, walls)
            if not path:
                ask.talk("Something went wrong and I couldn't find a path.")
                continue
            ask.talk("Press the following directions in order:")
            for direction in path:
                ask.talk(direction)
            return


class Password(ModuleSolver):
    """Solver for vanilla Password."""

    name: Final = "Password"
    id: Final = "Password"
    required_edgework: Final = ()

    valid_words: Final = {
        "about",
        "after",
        "again",
        "below",
        "could",
        "every",
        "first",
        "found",
        "great",
        "house",
        "large",
        "learn",
        "never",
        "other",
        "place",
        "plant",
        "point",
        "right",
        "small",
        "sound",
        "spell",
        "still",
        "study",
        "their",
        "there",
        "these",
        "thing",
        "think",
        "three",
        "water",
        "where",
        "which",
        "world",
        "would",
        "write",
    }

    def stage(self) -> None:
        while True:
            possible_words: List[str] = list(self.valid_words)
            for column_index in range(5):
                ask.talk("What letters are in column {0}?".format(column_index + 1))
                letters = ask.str_from_regex(r"[a-z]{6}")
                while len(set(letters)) != 6:  # all letters should be unique
                    ask.talk("There should be 6 unique letters in the column.")
                    ask.talk("What letters are in column {0}?".format(column_index + 1))
                    letters = ask.str_from_regex(r"[a-z]{6}")
                possible_words = [  # filter
                    word for word in possible_words if word[column_index] in letters
                ]
                if len(possible_words) == 1:
                    answer = possible_words[0].upper()
                    ask.talk('Enter the password "{0}".'.format(answer))
                    return
                if not possible_words:
                    break
            # no valid word or multiple valid words
            ask.talk("Something went wrong. Let's start over.")
