"Utilities relating to grids, grid sizes, and grid coordinates."

from string import ascii_lowercase
from typing import NamedTuple

from ktane.ask import talk
from ktane import ask

__all__ = ["Dimensions", "Coord", "ask_coord"]

class Dimensions(NamedTuple):
    "Size of a 2D square grid."
    rows: int
    cols: int

class Coord(NamedTuple):
    "A 0-indexed coordinate on a 2D square grid."
    row: int
    col: int

def ask_coord(*, alpha: bool = True) -> Coord:
    """Get a coordinate point from the user. If alpha is set (the default), the
    expected form is like "A5", otherwise, row and column are asked separately."""
    col: int
    row: int
    if alpha:
        talk('(Submit a coordinate like "B4", where the letter is the column')
        talk("and the number is the row.)")
        alpha_coord = ask.str_from_regex(r"[a-z][1-9][0-9]*")
        col = ascii_lowercase.index(alpha_coord[0]) + 1
        row = int(alpha_coord[1:])
    else:
        talk("Row number:")
        row = ask.positive_int()
        talk("Column number:")
        col = ask.positive_int()
    return Coord(row-1, col-1)
