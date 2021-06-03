import logging
from breezypythongui import EasyFrame
from drop_row import DropRow
from game_board import GameBoard
from game_controller import GameController

logging.basicConfig(level=logging.INFO)


class Connect4(EasyFrame):
    """
    Connect 4 game. The aim of the game for the players is to get
    four chips of their own colour in a row. "In a row" means
    horizontally, vertically, or diagonally.
    """
    def __init__(self):
        EasyFrame.__init__(self, title="Connect 4!", background='blue',
                           borderwidth=0, highlightthickness=0)

        drop_row = DropRow(self, 590, 100)
        self.addCanvas(drop_row, column=0, row=1)

        game_board = GameBoard(self, 590, 510)
        self.addCanvas(game_board, column=0, row=2)

        self.__game_controller = GameController(drop_row, game_board)


def main():
    connect4 = Connect4()
    connect4.mainloop()


if __name__ == '__main__':
    main()