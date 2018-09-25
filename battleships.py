"""Battleships!

This is the mighty game of battleships in text format.

First, each player sets up the board, then take turns to find
each other's ships!

Created by Marcus Croucher in 2018.

To do:

- [x] Create game loop / class
- [x] Create input functionality
- [X] Create win condition
- [X] Create display that doesn't show ships
- [X] Document functions
- [x] Decrease size
- [x] Increase ships
- [x] Feedback if full ship sunk
- [x] Feedback previous guess from previous player
- [x] Show current status (either hit rate or ships sunk).


"""
from itertools import cycle
import sys
import colorful
from board import Board
from const import LINE_LENGTH, START_SHIPS, SIZE, PROMPT
from const import HIT, MISS, SUNK, SHIP, EMPTY, BOARD_SEPERATOR
from const import Point, Ship

colorful.use_style("solarized")


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
                "\nHere is your board!"
                + f"\nShip number {number} is "
                + SHIP * ship
                + f" (length: {ship})"
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

            if orientation != "H" and orientation != "V":
                self.print_error("The orientation entered is not either H or V.")
                continue

            current_ship = Ship(start_position, ship, orientation)

            if not board.is_ship_on_board(current_ship):
                self.print_error("Some of the ship would fall outside of the board.")
                continue

            if board.check_ship_collisions(current_ship):
                self.print_error("The ship entered collides with another ship.")
                continue

            board.place_ship(current_ship)
            board.display()

            print("Would you like to keep the ship? (C) for confirm.")
            if input(PROMPT).upper() != "C":
                board.delete_ship(current_ship)
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

        clear_screen()
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

            if result == HIT or result == SUNK:
                if result == HIT:
                    print(colorful.green("You hit a ship! :)"))
                elif result == SUNK:
                    print(colorful.magenta("You SUNK a ship! :)"))

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

        text_template = "{}  | Score: {}"

        player_text = text_template.format(
            self.player_names[player], self.boards[other_player].hits
        )

        other_player_text = text_template.format(
            self.player_names[other_player], self.boards[player].hits
        )

        player_header = center(colorful.blue(player_text))
        other_player_header = center(colorful.red(other_player_text))

        print(player_header + (" " * len(BOARD_SEPERATOR)) + other_player_header)

        for this_board, other_board in zip(this_board_display, other_board_display):
            print(this_board + BOARD_SEPERATOR + other_board)

    def demo_setup(self):
        """Demo game for testing player turns."""
        self.player_names = {"A": "Marcus", "B": "Rose"}

        for player in self.players:
            self.boards[player].place_ship(Ship((1, 1), 4, "H"))
            self.boards[player].place_ship(Ship((2, 1), 4, "H"))


if __name__ == "__main__":
    if "test" in sys.argv:
        Game(True)
    else:
        Game()
