"""Battleships using the pyxel engine.

To dos

[ ] Create artwork
[ ] Create interface / board
[ ] Create method for placing battleships
[ ] Create method for selecting place to hit / displaying board


"""

import pyxel


class App:
    def __init__(self):
        pyxel.init(160, 120)
        self.x = 0
        pyxel.run(self.update, self.draw)

    ### Update methods ############################################

    def update(self):
        self.x = (self.x + 1) % pyxel.width

    ### Draw methods ##############################################

    def draw(self):
        self.draw_background()

    def draw_background(self):
        pass


if __name__ == "__main__":
    App()
