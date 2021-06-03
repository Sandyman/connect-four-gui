import logging
from drop_row import DropRow
from four_in_a_row import FourInARow
from game_board import GameBoard

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class GameController:
    COLUMNS = 7
    ROWS = 6

    def __init__(self, drop_row: DropRow, game_board: GameBoard, p1='yellow', p2='red'):
        self.__four_in_a_row = FourInARow(cols=7, rows=6)
        self.__drop_row = drop_row
        self.__game_board = game_board

        self.__player_1_colour = p1
        self.__player_2_colour = p2

        self.__current_player = 1
        self.__current_colour = p1

        self.__drop_row.set_active_colour(self.__current_colour)

        drop_row.set_click_handler(self.__column_clicked)

        self.__columns = [list() for _ in range(self.COLUMNS)]

    def __column_clicked(self, column):
        logger.info(f'Column {column} clicked!')

        selected_column = self.__columns[column]
        row = len(selected_column)
        if row >= self.ROWS:
            logger.warning(f'Column {column} is full!')
            return

        logger.info(f'Valid move: (col,row)=({column},{row})')

        # Update the cell on the board
        self.__game_board.update_cell(column, row, self.__current_colour)
        selected_column.append(self.__current_colour)

        # Disable the column if it's full
        if len(selected_column) == self.ROWS:
            logger.info(f'Disabling column {column} since it\'s full.')
            self.__drop_row.disable_column(column)

        # Next player is up
        self.__switch_player()

    def __switch_player(self):
        """
        Switch player. This also switches the colour for convenience.
        """
        self.__current_player = 2 if self.__current_player == 1 else 1

        if self.__current_player == 1:
            self.__current_colour = self.__player_1_colour
        else:
            self.__current_colour = self.__player_2_colour

        self.__drop_row.set_active_colour(self.__current_colour)
