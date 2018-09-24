"""Constants for the battleship game."""

from collections import namedtuple
import colorful

colorful.use_style("solarized")

SIZE = 9
LINE_LENGTH = (SIZE * 3) + 3
EMPTY = "-"
SHIP = "S"
HIT = "H"
MISS = "M"
SUNK = "Sunk"

BOARD_COLOURS = {
    SHIP: colorful.blue,
    HIT: colorful.red,
    MISS: colorful.violet,
    EMPTY: colorful.base02,
    "recent": colorful.yellow,
}

SEPERATOR = "  "
BOARD_SEPERATOR = colorful.cyan("  --|--  ")

PROMPT = colorful.orange(">>> ")

START_SHIPS = [7, 5, 4, 4, 3, 2]

Point = namedtuple("Point", "x y")
Ship = namedtuple("Ship", "position length orientation")
