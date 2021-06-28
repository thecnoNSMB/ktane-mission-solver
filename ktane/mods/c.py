"Modded modules whose names begin with the letter C."

from typing import Final

from ktane.directors import ModuleSolver
from ktane.ask import talk
from ktane import ask

__all__ = [
    "ColourFlash",
    "CrazyTalk",
]

class ColourFlash(ModuleSolver):
    "Solver for Colour Flash."
    name: Final = "Colour Flash"
    id: Final = "ColourFlash"
    required_edgework: Final = ()

    valid_colors: Final = {"red", "yellow", "green", "blue", "magenta", "white"}

    def stage(self) -> None: #pylint: disable=too-many-branches #can't help it
        talk("What color is the last word in the sequence?")
        last_color = ask.str_from_set(self.valid_colors)
        if last_color == "red":
            if ask.yes_no("Does the word Green appear at least three times?"):
                talk("Press Yes on the third word whose color or text is green.")
            elif ask.yes_no("Is there exactly one blue-colored word?"):
                talk("Press No on the word Magenta.")
            else:
                talk("Press Yes on the last word whose color or text is white.")
        elif last_color == "yellow":
            if ask.yes_no("Does the word Blue appear colored green?"):
                talk("Press Yes on the first word colored green.")
            elif ask.yes_no("Does the word White appear colored white or red?"):
                talk("Press Yes on the second word whose color doesn't match its text.")
            else:
                talk("Count the number of words whose color or text is magenta.")
                talk("Press No that many words into the sequence.")
        elif last_color == "green":
            if ask.yes_no("Does a word appear twice in a row with different colors?"):
                talk("Press No on the fifth word in the sequence.")
            elif ask.yes_no("Does the word Magenta appear at least three times?"):
                talk("Press No on the first word whose color or text is yellow.")
            else:
                talk("Press Yes on any word whose text matches its color.")
        elif last_color == "blue":
            if ask.yes_no("Are there at least three words whose"
                          " color doesn't match their text?"):
                talk("Press Yes on the first such word.")
            elif (ask.yes_no("Does the word Red appear colored yellow?")
                  or ask.yes_no("Does the word Yellow appear colored white?")):
                talk("Press No on the word White that is colored red.")
            else:
                talk("Press Yes on the last word whose color or text is green.")
        elif last_color == "magenta":
            if ask.yes_no("Do two words in a row share a color?"):
                talk("Press Yes on the third word.")
            elif ask.yes_no("Are there more words reading Yellow"
                            " than words colored blue?"):
                talk("Press No on the last word whose text is Yellow.")
            else:
                talk("Note the text of the seventh word.")
                talk("Press No on the first word with that color.")
        else: #white
            if ask.yes_no("Does the third word's color match"
                          " the fourth or fifth words' text?"):
                talk("Press No on the first word whose color or text is blue.")
            elif ask.yes_no("Does the word Yellow appear colored red?"):
                talk("Press Yes on the last word colored blue.")
            else:
                talk("Press No at any time.")

class CrazyTalk(ModuleSolver):
    "Solver for Crazy Talk."
    name: Final = "Crazy Talk"
    id: Final = "CrazyTalk"
    required_edgework: Final = ()

    table: Final = {
        "< < > < > >": (5, 4),
        "1 3 2 4": (3, 2),
        "left arrow left word right arrow left word right arrow right word": (5, 8),
        "blank": (1, 3),
        "literally blank": (1, 5),
        "for the love of all that is good and holy please fullstop fullstop.": (9, 0),
        "an actual left arrow literal phrase": (5, 3),
        "for the love of - the display just changed, i didn't know this mod could do "
        "that. does it mention that in the manual?": (8, 7),
        "all words one three to for for as in this is for you": (4, 0),
        "literally nothing": (1, 4),
        "no, literally nothing": (2, 5),
        "the word left": (7, 0),
        "hold on it's blank": (1, 9),
        "seven words five words three words the punctuation fullstop": (0, 5),
        "the phrase the word stop twice": (9, 1),
        "the following sentence the word nothing": (2, 7),
        "one three to for": (3, 9),
        "three words the word stop": (7, 3),
        "disregard what i just said. four words, no punctuation. one three 2 4.": (3, 1),
        "1 3 2 for": (1, 0),
        "disregard what i just said. two words then two digits. one three 2 4.": (0, 8),
        "we just blew up": (4, 2),
        "no really.": (5, 2),
        "< left > left > right": (5, 6),
        "one and then 3 to 4": (4, 7),
        "stop twice": (7, 6),
        "left": (6, 9),
        "..": (8, 5),
        "period period": (8, 2),
        "there are three words no punctuation ready? stop dot period": (5, 0),
        "novebmer oscar space, lima indigo tango echo romeo alpha lima lima yankee space "
        "november oscar tango hotel indego november golf": (2, 9),
        "five words three words the punctuation fullstop": (1, 9),
        "the phrase: the punctuation fullstop": (9, 3),
        "empty space": (1, 6),
        "one three two four": (3, 7),
        "it's showing nothing": (2, 3),
        "lima echo foxtrot tango space alpha romeo romeo oscar risky space sierra yankee "
        "mike bravo oscar lima": (1, 2),
        "one 3 2 4": (3, 4),
        "stop.": (7, 4),
        ".period": (8, 1),
        "no really stop": (5, 1),
        "1 3 too 4": (2, 0),
        "period twice": (8, 3),
        "1 3 too with 2 ohs four": (4, 2),
        "1 3 to 4": (3, 0),
        "stop dot period": (5, 0),
        "left left right left right right": (6, 7),
        "it literally says the word one and then the numbers 2 3 4": (4, 5),
        "one in letters 3 2 4 in numbers": (3, 5),
        "wait forget everything i just said, two words then two symbols then two words: "
        "< < right left > >": (1, 6),
        "1 three two four": (3, 6),
        "period": (7, 9),
        ".stop": (7, 8),
        "novebmer oscar space, lima india tango echo romeo alpha lima lima yankee space "
        "november oscar tango hotel india november golf": (0, 7),
        "lima echo foxtrot tango space alpha romeo romeo oscar whiskey space sierra "
        "yankee mike bravo oscar lima": (6, 5),
        "nothing": (1, 2),
        "there's nothing": (1, 8),
        "stop stop": (7, 5),
        "right all in words starting now one two three four": (4, 9),
        "the phrase the word left": (7, 1),
        "left arrow symbol twice then the words right left right then a right arrow "
        "symbol": (5, 9),
        "left left right < right >": (5, 7),
        "no comma literally nothing": (2, 4),
        "hold on crazy talk while i do this needy": (2, 1),
        "this one is all arrow symbols no words": (2, 8),
        "<": (6, 3),
        "the word stop twice": (9, 4),
        "< < right left > >": (6, 1),
        "the punctuation fullstop": (9, 2),
        "1 3 too with two os 4": (4, 1),
        "three words the punctuation fullstop": (9, 9),
        "ok word for word left arrow symbol twice then the words right left right then a "
        "right arrow symbol": (6, 0),
        "dot dot": (8, 6),
        "left arrow": (6, 8),
        "after i say beep find this phrase word for word beep an actual left "
        "arrow": (7, 2),
        "one three 2 with two ohs 4": (4, 3),
        "left arrow symbol": (6, 4),
        "an actual left arrow": (6, 2),
        "that's what it's showing": (2, 1),
        "the phrase the word nothing": (2, 6),
        "the word one and then the numbers 3 2 4": (4, 8),
        "one 3 2 four": (3, 8),
        "one word then punctuation. stop stop.": (0, 9),
        "the word blank": (0, 1),
        "fullstop fullstop": (8, 4)
    }

    def stage(self) -> None:
        talk("What is on the display? Type it exactly as written.")
        talk("Include any typos. Type arrows as angle brackets.")
        phrase = ask.str_from_set(self.table.keys())
        talk("Flip the switch down when the bomb "
             f"timer has a {self.table[phrase][0]} in the seconds column.")
        talk("Then, flip the switch up when the bomb "
             f"timer has a {self.table[phrase][1]} in the seconds column.")
