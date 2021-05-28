from breezypythongui import EasyFrame
from drop_row import DropRow
from game_board import GameBoard


class Connect4(EasyFrame):
    def __init__(self):
        EasyFrame.__init__(self, title="Connect 4!", background='blue',
                           borderwidth=0, highlightthickness=0)

        self.addCanvas(DropRow(self, 590, 100), column=0, row=0)
        self.addCanvas(GameBoard(self, 590, 510), column=0, row=1)


def main():
    connect4 = Connect4()
    connect4.mainloop()


if __name__ == '__main__':
    main()
