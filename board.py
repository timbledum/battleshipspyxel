"""Define board class to keep track of the status of the board."""

from string import ascii_uppercase
from const import EMPTY, SHIP, HIT, MISS, SUNK, SEPERATOR, BOARD_COLOURS
from const import Point, Ship


class Board:
    def __init__(self, size):
        """Set up key variables."""

        self.size = size
        self.ships = {}
        self.guesses = []
        self.hits = 0

    def is_on_board(self, position):
        """Return True if the position is on the board."""
        for coordinate in position:
            if not (0 <= coordinate < self.size):
                return False
        return True

    def is_ship_on_board(self, ship):
        """Return True if ship fits on the board."""

        row, column = ship.position

        if ship.orientation == "H":
            long, short = column, row
        elif ship.orientation == "V":
            long, short = row, column

        if short > self.size:
            return False

        if long + ship.length > self.size:
            return False

        for direction in ship.position:
            if direction < 0:
                return False

        return True

    @staticmethod
    def generate_ship(ship):
        """Generate a ship as a list of coordinates."""

        row, column = ship.position

        ship_positions = []
        for i in range(ship.length):
            if ship.orientation == "H":
                ship_positions.append(Point(row, column + i))
            elif ship.orientation == "V":
                ship_positions.append(Point(row + i, column))

        return ship_positions

    def check_ship_collisions(self, ship):  # TODO
        """Check if the current ship overlaps any other ships."""

        for other_ship in self.ships:
            other_ship_set = set(self.generate_ship(other_ship))
            current_ship_set = set(self.generate_ship(ship))
            if not other_ship_set.isdisjoint(current_ship_set):
                return True
        return False

    def place_ship(self, ship):
        """Place the current ship on the board."""
        self.ships[ship] = ship.length

    def delete_recent_ship(self, ship):
        """Delete the current ship from the board."""
        del self.ships[ship]

    def is_guessed(self, position):
        """Return True if the position has already been guessed."""

        return position in self.guesses

    def guess_position(self, position):
        """Accepts game position and updates board. Also return hit/miss."""

        self.guesses.append(position)

        for ship in self.ships:
            if position in self.generate_ship(ship):
                self.ships[ship] -= 1
                if self.ships[ship] == 0:
                    result = SUNK
                else:
                    result = HIT
                self.hits += 1
                break
        else:
            result = MISS

        return result

    def print_rows(self, show_ships=True):
        """Return a generator that produces the rows in the board."""

        seperator_length = len(SEPERATOR) + 1
        column_headers = "".join(
            [str(i).ljust(seperator_length) for i in range(1, self.size + 1)]
        )

        yield "   " + column_headers

        for row in range(self.size):
            row_letter = ascii_uppercase[row]

            row_text = ""
            for column in range(self.size):
                current_position = Point(row, column)

                for ship in self.ships:
                    if current_position in self.generate_ship(ship):
                        if current_position in self.guesses:
                            value = HIT
                        else:
                            if show_ships:
                                value = SHIP
                            else:
                                value = EMPTY
                        break
                else:
                    if current_position in self.guesses:
                        value = MISS
                    else:
                        value = EMPTY

                color_applier = BOARD_COLOURS[value]
                if self.guesses:
                    if current_position == self.guesses[-1]:
                        color_applier = BOARD_COLOURS["recent"]

                value = color_applier(value)
                row_text += value + SEPERATOR

            yield row_letter + "  " + row_text

    def display(self, show_ships=True):
        """Display the board."""

        for row in self.print_rows(show_ships):
            print(row)

    def all_ships_sunk(self):
        """Return True if all ships have been sunk."""

        for ship_health in self.ships.values():
            if ship_health > 0:
                return False
        return True

    @staticmethod
    def convert_position(position):
        """Convert position from 'C6' notation to (2, 5) format."""
        row = position[0]
        column = position[1:]

        row_number = ascii_uppercase.index(row)
        column_number = int(column) - 1

        return Point(row_number, column_number)
