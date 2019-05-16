"""Constants for the battleship game."""

from collections import namedtuple


SIZE = 9
BOX_SIZE = 16
EMPTY = "-"
SHIP = "S"
HIT = "H"
MISS = "M"
SUNK = "Sunk"

START_SHIPS = [7, 5, 4, 4, 3, 2]

Point = namedtuple("Point", "x y")
Ship = namedtuple("Ship", "position length orientation")


### Pyxel colours #############################################

C_OCEAN_LINE
C_OCEAN
