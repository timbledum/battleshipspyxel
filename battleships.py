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
                
                collision = False
                for r, c in ship_positions:
                    if self.board[r][c] == SHIP:
                        collision = True
                        break
                
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


    def display(self):
        seperator_length = len(SEPERATOR) + 1
        column_headers = "".join([str(i).ljust(seperator_length) for i in range(1, self.size + 1)])
        print("  ", column_headers) 
        for row_index, row in enumerate(self.board):
            row_letter = ascii_uppercase[row_index]
            row_text = ""
            for column in row:
                row_text += column + SEPERATOR
            print(row_letter + " ", row_text)

    @staticmethod
    def convert_position(position):
        row, column = position
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