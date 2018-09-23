"""Battleships!

To do:

- [ ] Create game loop / class
- [ ] Create input functionality
- [ ] Create win condition
- [ ] Create display that doesn't show ships
- [ ] Document functions


"""
from string import ascii_uppercase
from random import randint, choice
from itertools import cycle
from textwrap import dedent
import colorful

colorful.use_style("solarized")

SIZE = 10
LINE_LENGTH = (SIZE * 3) + 3
EMPTY = "-"
SHIP = colorful.blue("S")
HIT = colorful.red("H")
MISS = colorful.violet("M")
SEPERATOR = "  "

PROMPT = colorful.orange(">>> ")

START_SHIPS = [2, 2, 4, 4, 5]


def clear_screen():
    print("\n" * 100)


def center(text, width=LINE_LENGTH):
    length = len(text)
    start = (width - length) // 2
    end = width - length - start
    output = (" " * start) + text + (" " * end)
    return output


class Board:
    def __init__(self, size):
        self.size = size
        self.board = [[EMPTY for _ in range(size)] for _ in range(size)]

    def is_ship_on_board(self, ship_start, ship_length, orientation):
        """Return yes if ship fits on the board."""
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

    def generate_ship(self, ship_start, ship_length, orientation):
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

    def guess_position(self, position):
        """Accepts game position and updates board. Also return hit/miss."""
        row, column = self.convert_position(position)
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
        for row in self.print_rows(show_ships):
            print(row)

    @staticmethod
    def convert_position(position):
        """Convert position from 'C6' notation to (2, 5) format."""
        row = position[0]
        column = position[1:]

        row_number = ascii_uppercase.index(row)
        column_number = int(column) - 1

        return (row_number, column_number)


class Game:
    def __init__(self):

        # Set up the variables
        self.players = "AB"
        self.player_names = {}
        self.boards = {player: Board(SIZE) for player in self.players}
        self.ships = START_SHIPS

        self.welcome()

        # Set up the players
        for player in self.players:
            self.set_up(player)

        # Play the game
        for player in cycle(self.players):
            if self.round(player):
                break

    def welcome(self):
        """Print the initial input screen and wait for initial input."""

        clear_screen()

        text = (
            ("#" * LINE_LENGTH + "\n" * 2)
            + center(colorful.base02("Welcome to ") + colorful.green("battleships") + colorful.base02("!!!"))
            + "\n"
            + ""
            + "\n"
            + center(colorful.base02("A game of ") + colorful.red("naval battles"))
            + "\n"
            + center(colorful.base02("and ") + colorful.blue("sea adventures") + colorful.base02("."))
            + "\n"
            + "\n"
            + "\n"
            + center(
                colorful.base02("Hit ")
                + colorful.orange("ENTER")
                + colorful.base02(" to begin.")
            )
            + "\n"
            + "\n"
            + "#" * LINE_LENGTH
            + "\n"
        )
        print(text)
        input()

    def set_up(self, player):
        """Allow the players to set up their screens."""
        clear_screen()
        board = self.boards[player]

        input(f"Pass the computer to player {player}. Hit ENTER when ready.")

        print("What would you like to be called?")
        self.player_names[player] = input(PROMPT)

        clear_screen()

        for number, ship in enumerate(self.ships, start=1):
            self.set_ship(player, ship, number)


    def set_ship(self, player, ship, number):
        """Set up one ship, including validating input."""

        board = self.boards[player]

        while True:
            board.display()
            print(
                "\nHere is your board."
                + f"\nShip number {number} is "
                + SHIP * ship
                + "\nEnter the start point of the ship (i.e., A1)"
            )
            start_point = input(PROMPT).upper()

            print("Enter the orientation of the ship" "\n(H)orizontal or (V)ertical")
            orientation = input(PROMPT).upper()

            # Checks
            try:
                start_position = board.convert_position(start_point)
            except BaseException:
                self.print_error("The start position is invalid.")
                continue

            if not board.is_ship_on_board(start_position, ship, orientation):
                self.print_error("Some of the ship would fall outside of the board.")
                continue

            if orientation not in "HV" and orientation is not "HV":
                self.print_error("The orientation entered is not either H or V.")
                continue

            ship_positions = board.generate_ship(start_position, ship, orientation)

            if board.check_ship_collisions(ship_positions):
                self.print_error("The ship entered collides with another ship.")
                continue

            board.place_ship(ship_positions)
            board.display()

            print("Would you like to keep the ship? (C) for confirm.")
            if input(PROMPT).upper() != "C":
                board.delete_ship(ship_positions)
                continue
            else:
                break

    @staticmethod
    def print_error(error):
        """Print the error message if invalid input."""
        print(colorful.red("Error ") + colorful.base02(f"- {error} Please try again."))
        input()

    def round(self, player):
        return True


if __name__ == "__main__":
    Game()
