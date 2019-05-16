"""Battleships using the pyxel engine.

To dos

[ ] Create artwork
[ ] Create interface / board
[ ] Create method for placing battleships
[ ] Create method for selecting place to hit / displaying board


"""

import pyxel

import const


class App:
    def __init__(self):
        self.game_box = const.SIZE * const.BOX_SIZE
        pyxel.init(self.game_box, self.game_box + const.SCORE_HEIGHT)

        self.selection = None
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    ### Update methods ############################################

    def update(self):
        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()
        self.update_selection_box()

    def update_selection_box(self):
        """Update the selection box.

        Only have a selection if the mouse is in the game box and if 
        the mouse is not on a line."""

        x, sub_x = divmod(pyxel.mouse_x, const.BOX_SIZE)
        y, sub_y = divmod(pyxel.mouse_y, const.BOX_SIZE)

        if sub_x in (0, 15) or sub_y in (0, 15):
            self.selection = None
            return

        if not (0 <= x < const.SIZE and 0 <= y < const.SIZE):
            self.selection = None
            return

        self.selection = x, y

    ### Draw methods ##############################################

    def draw(self):
        self.draw_background()
        self.draw_selection()

    def draw_background(self):
        """Draw background and grid."""
        pyxel.cls(const.C_OCEAN)

        game_box = self.game_box - 1

        # Draw lines
        for i in range(const.SIZE):
            position1 = i * const.BOX_SIZE
            position2 = position1 + const.BOX_SIZE - 1

            col = const.C_OCEAN_LINE
            pyxel.line(x1=position1, y1=0, x2=position1, y2=game_box, col=col)
            pyxel.line(x1=position2, y1=0, x2=position2, y2=game_box, col=col)
            pyxel.line(x1=0, y1=position1, x2=game_box, y2=position1, col=col)
            pyxel.line(x1=0, y1=position2, x2=game_box, y2=position2, col=col)

        # Draw scorebox
        col = const.C_SCOREBOX
        height = game_box + const.SCORE_HEIGHT
        pyxel.rectb(x1=0, y1=game_box + 1, x2=game_box, y2=height, col=col)

    def draw_selection(self):
        """Draw the selected position of the mouse."""

        if self.selection:
            x, y = self.selection
            x, y = x * const.BOX_SIZE, y * const.BOX_SIZE
            pyxel.rect(x1=x + 1, x2=x + 14, y1=y + 1, y2=y + 14, col=const.C_SELECTION)


if __name__ == "__main__":
    App()
