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
        self.x = 0
        pyxel.run(self.update, self.draw)

    ### Update methods ############################################

    def update(self):
        self.x = (self.x + 1) % pyxel.width

    ### Draw methods ##############################################

    def draw(self):
        self.draw_background()

    def draw_background(self):
        """Draw background and grid."""
        pyxel.cls(const.C_OCEAN)

        # Draw lines
        width = self.game_box - 1
        for i in range(const.SIZE):
            position1 = i * const.BOX_SIZE
            position2 = position1 + const.BOX_SIZE - 1

            col = const.C_OCEAN_LINE
            pyxel.line(x1=position1, y1=0, x2=position1, y2=width, col=col)
            pyxel.line(x1=position2, y1=0, x2=position2, y2=width, col=col)
            pyxel.line(x1=0, y1=position1, x2=width, y2=position1, col=col)
            pyxel.line(x1=0, y1=position2, x2=width, y2=position2, col=col)


if __name__ == "__main__":
    App()
