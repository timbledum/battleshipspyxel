"""Battleships!

To do:

- [x] Create game loop / class
- [x] Create input functionality
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
BOARD_SEPERATOR = colorful.cyan("  --|--  ")

PROMPT = colorful.orange(">>> ")

START_SHIPS = [2, 2, 4, 4, 5]


def clear_screen():
    """Clear the screen."""

    print("\n" * 100)


def center(text, width=LINE_LENGTH):
    """Centre colorful strings."""

    length = len(text)
    start = (width - length) // 2
    end = width - length - start
    output = (" " * start) + text + (" " * end)
    return output


class Board:
    def __init__(self, size):
        """Set up key variables."""

        self.size = size
        self.board = [[EMPTY for _ in range(size)] for _ in range(size)]

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


class Game:
    def __init__(self, testing=False):
        """Set up key variables and play the game."""

        # Set up the variables
        self.players = "AB"
        self.player_names = {}
        self.boards = {player: Board(SIZE) for player in self.players}
        self.ships = START_SHIPS

        self.welcome()


        # Set up the players
        if testing:
            self.demo_setup()
        else:
            for player in self.players:
                self.set_up(player)


        # Play the game
        for player in cycle(self.players):
            if self.round(player):
                break

        winning_player = colorful.magenta(self.player_names[player])
        print(winning_player + " is the " + colorful.red("WINNER!!!"))
        input()

    def welcome(self):
        """Print the initial input screen and wait for initial input."""

        clear_screen()

        text = (
            ("#" * LINE_LENGTH + "\n" * 2)
            + center(
                colorful.base02("Welcome to ")
                + colorful.green("battleships")
                + colorful.base02("!!!")
            )
            + "\n"
            + ""
            + "\n"
            + center(colorful.base02("A game of ") + colorful.red("naval battles"))
            + "\n"
            + center(
                colorful.base02("and ")
                + colorful.blue("sea adventures")
                + colorful.base02(".")
            )
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

    ####################
    # Set up the board #
    ####################

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

            if orientation not in "HV" and orientation is not "HV":
                self.print_error("The orientation entered is not either H or V.")
                continue

            if not board.is_ship_on_board(start_position, ship, orientation):
                self.print_error("Some of the ship would fall outside of the board.")
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

    #################
    # Play the game #
    #################

    def round(self, player):
        """Go through one round of battleships."""

        player_name = colorful.violet(self.player_names[player])
        other_player = self.players.replace(player, "")

        board = self.boards[player]
        other_board = self.boards[other_player]

        clear_screen()
        input(f"Pass the computer to {player_name}. Hit ENTER when ready.")

        print(f"Hello {player_name}.")

        while True:
            self.display_both_boards(player)

            print("Please enter your guess.")
            guess = input(PROMPT).upper()

            try:
                guess_position = other_board.convert_position(guess)
            except BaseException:
                self.print_error("The position entered is invalid.")
                continue

            if not other_board.is_on_board(guess_position):
                self.print_error("The guess is outside of the board.")
                continue

            if other_board.is_guessed(guess_position):
                self.print_error("This position has already been guessed.")
                continue

            result = other_board.guess_position(guess_position)

            if result == HIT:
                print(colorful.green("You hit a ship! :)"))
                input()
                if other_board.all_ships_sunk():
                    return True
            elif result == MISS:
                print(colorful.blue("You missed any ships... :'("))
                input()
                break

        else:
            return False

    def display_both_boards(self, player):
        """Display the current board on the left and the other board on the right."""

        other_player = self.players.replace(player, "")

        this_board_display = self.boards[player].print_rows(show_ships=True)
        other_board_display = self.boards[other_player].print_rows(show_ships=False)

        player_name = self.player_names[player]
        other_player_name = self.player_names[other_player]

        player_header = center(colorful.blue(player_name))
        other_player_header = center(colorful.red(other_player_name))

        print(player_header + (" " * len(BOARD_SEPERATOR)) + other_player_header)

        for this_board, other_board in zip(this_board_display, other_board_display):
            print(this_board + BOARD_SEPERATOR + other_board)


    def demo_setup(self):
        """Demo game for testing player turns."""
        self.player_names = {"A": "Marcus", "B": "Rose"}

        self.boards["A"].place_ship(self.boards["A"].generate_ship((1,1), 4, "H"))
        self.boards["A"].place_ship(self.boards["A"].generate_ship((2,1), 4, "H"))

        self.boards["B"].place_ship(self.boards["B"].generate_ship((1,1), 4, "H"))
        self.boards["B"].place_ship(self.boards["B"].generate_ship((2,1), 4, "H"))


if __name__ == "__main__":
    Game()
