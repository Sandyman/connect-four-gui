import logging
from breezypythongui import EasyFrame
from drop_row import DropRow
from game_board import GameBoard
from game_controller import GameController
from player import Player
from player_list import PlayerList

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Connect4(EasyFrame):
    """
    Connect 4 game. The aim of the game for the players is to get
    four chips of their own colour in a row. "In a row" means
    horizontally, vertically, or diagonally.
    """
    COLUMNS = 7
    ROWS = 6

    def __init__(self):
        EasyFrame.__init__(self, title="Connect 4!", background='blue',
                           borderwidth=0, highlightthickness=0)

        # Create the drop (from where we "drop" the coloured chips)
        drop_row = DropRow(self, 590, 100, columns=self.COLUMNS)
        self.addCanvas(drop_row, column=0, row=1)

        # Create the actual game board
        game_board = GameBoard(self, 590, 510, columns=self.COLUMNS,
                               rows=self.ROWS)
        self.addCanvas(game_board, column=0, row=2)

        # Create Player objects, PlayerList, and iterator
        p1, p2 = Player('yellow'), Player('red')
        player_list = iter(PlayerList(p1, p2))

        # The controller ties it all together
        controller = GameController(self, drop_row,
                                    game_board, player_list,
                                    self.COLUMNS, self.ROWS)
        self.__game_controller = controller

    def game_over(self, player=None):
        """
        Called by the GameController when the game is over. If
        there was a winner, the player argument is a reference
        to the winning player, otherwise it's set to None.

        :param player: Player who won the game
        """
        score = None if player is None else player.score
        logger.info(f'Game over. Score={score}.')


def main():
    connect4 = Connect4()
    connect4.mainloop()


if __name__ == '__main__':
    main()
