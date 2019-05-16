"""Constants for the battleship game."""

from collections import namedtuple


SIZE = 9
BOX_SIZE = 16
SCORE_HEIGHT = 16

EMPTY = "-"
SHIP = "S"
HIT = "H"
MISS = "M"
SUNK = "Sunk"

START_SHIPS = [7, 5, 4, 4, 3, 2]

Point = namedtuple("Point", "x y")
Ship = namedtuple("Ship", "position length orientation")


### Pyxel colours #############################################

BLACK = 0
NAVY = 1
PURPLE = 2
GREEN = 3
BROWN = 4
GREY = 5
SILVER = 6
WHITE = 7
RED = 8
ORANGE = 9
YELLOW = 10
LIME = 11
BLUE = 12
LAVENDER = 13
PINK = 14
TAN = 15

C_OCEAN_LINE = BLUE
C_OCEAN = NAVY
C_SCOREBOX = SILVER
C_SELECTION = LAVENDER
