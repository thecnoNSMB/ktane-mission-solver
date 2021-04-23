"Modded modules whose names begin with the letter C."

from typing import Final

from ktane.directors import ModuleSolver
from ktane.ask import talk
from ktane import ask

__all__ = [
    "ColourFlash",
]

class ColourFlash(ModuleSolver):
    "Solver for Colour Flash."
    name: Final = "Colour Flash"
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
