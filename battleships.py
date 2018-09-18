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
import colorful

colorful.use_style('solarized')

SIZE = 10
EMPTY = "-"
SHIP = colorful.blue("S")
HIT = colorful.red("H")
MISS = colorful.violet("M")
SEPERATOR = "  "

START_SHIPS = [2, 2, 4, 4, 5]


class Board:
    def __init__(self, size):
        self.size = size
        self.board = [[EMPTY for _ in range(size)] for _ in range(size)]

    def set_up_board(self):
        """Place ships randomly in grid."""
        for ship in START_SHIPS:

            collision = True
            while collision:
                orientation = choice("HV")

                # Assuming horizontal
                row, column = randint(0, self.size - 1), randint(0, self.size - 1 - ship)

                ship_positions = []
                for i in range(ship):
                    ship_positions.append((row, column + i))
                
                # Convert to vertical
                if orientation == "V":
                    ship_positions = [(c, r) for r, c in ship_positions]
                
                # Check whether position overlaps existing ship
                collision = False
                for r, c in ship_positions:
                    if self.board[r][c] == SHIP:
                        collision = True
                        break
                
                # Create ship onto board if position valid
                if not collision:
                    for r, c in ship_positions:
                        self.board[r][c] = SHIP


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
        column_headers = "".join([str(i).ljust(seperator_length) for i in range(1, self.size + 1)])
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

if __name__ == "__main__":
    board = Board(12)
    board.set_up_board()
    board.guess_position("E9")
    board.guess_position("D2")
    board.guess_position("A1")
    board.guess_position("G6")
    board.display()