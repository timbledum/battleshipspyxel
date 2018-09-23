"""Constants for the battleship game."""

import colorful

colorful.use_style("solarized")

SIZE = 9
LINE_LENGTH = (SIZE * 3) + 3
EMPTY = "-"
SHIP = colorful.blue("S")
HIT = colorful.red("H")
MISS = colorful.violet("M")
SEPERATOR = "  "
BOARD_SEPERATOR = colorful.cyan("  --|--  ")

PROMPT = colorful.orange(">>> ")

START_SHIPS = [7, 5, 4, 4, 3, 2]