"""Define board class to keep track of the status of the board."""

from string import ascii_uppercase
from const import EMPTY, SHIP, HIT, MISS, SEPERATOR

class Board:
    def __init__(self, size):
        """Set up key variables."""

        self.size = size
        self.board = [[EMPTY for _ in range(size)] for _ in range(size)]
        self.ships = []

    def is_on_board(self, position):
        """Return True if the position is on the board."""
        for coordinate in position:
            if 0 < coordinate < self.size:
                return True
        return False

    def is_ship_on_board(self, ship_start, ship_length, orientation):
        """Return True if ship fits on the board."""

        row, column = ship_start

        if orientation == "H":
            long, short = column, row
        elif orientation == "V":
            long, short = row, column

        if short > self.size:
            return False

        if long + ship_length > self.size:
            return False

        for direction in ship_start:
            if direction < 0:
                return False

        return True

    @staticmethod
    def generate_ship(ship_start, ship_length, orientation):
        """Generate a ship as a list of coordinates."""

        row, column = ship_start

        ship_positions = []
        for i in range(ship_length):
            if orientation == "H":
                ship_positions.append((row, column + i))
            elif orientation == "V":
                ship_positions.append((row + i, column))

        return ship_positions

    def check_ship_collisions(self, ship_positions):
        """Check if the current ship overlaps any other ships."""

        for r, c in ship_positions:
            if self.board[r][c] == SHIP:
                return True
        return False

    def place_ship(self, ship_positions):
        """Place the current ship on the board."""

        for r, c in ship_positions:
            self.board[r][c] = SHIP

    def delete_ship(self, ship_positions):
        """Delete the current ship from the board."""

        for r, c in ship_positions:
            self.board[r][c] = EMPTY

    def is_guessed(self, position):
        """Return True if the position has already been guessed."""
        r, c = position
        return self.board[r][c] in [MISS, HIT]

    def guess_position(self, position):
        """Accepts game position and updates board. Also return hit/miss."""

        row, column = position
        current_status = self.board[row][column]
        if current_status in (SHIP, HIT):
            result = HIT
        else:
            result = MISS

        self.board[row][column] = result
        return result

    def print_rows(self, show_ships=True):
        """Return a generator that produces the rows in the board."""

        seperator_length = len(SEPERATOR) + 1
        column_headers = "".join(
            [str(i).ljust(seperator_length) for i in range(1, self.size + 1)]
        )
        yield "   " + column_headers

        for row_index, row in enumerate(self.board):
            row_letter = ascii_uppercase[row_index]
            row_text = ""
            for column in row:
                if column == SHIP and not show_ships:
                    row_text += EMPTY + SEPERATOR
                else:
                    row_text += column + SEPERATOR

            yield row_letter + "  " + row_text

    def display(self, show_ships=True):
        """Display the board."""

        for row in self.print_rows(show_ships):
            print(row)

    def all_ships_sunk(self):
        """Return True if all ships have been sunk."""

        for row in self.board:
            if SHIP in row:
                return False
        return True

    @staticmethod
    def convert_position(position):
        """Convert position from 'C6' notation to (2, 5) format."""
        row = position[0]
        column = position[1:]

        row_number = ascii_uppercase.index(row)
        column_number = int(column) - 1

        return (row_number, column_number)
