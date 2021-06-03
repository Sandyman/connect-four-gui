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

        winner = self.__check_four_in_a_row(column, row)

        # Disable the column if it's full
        if len(selected_column) == self.ROWS:
            logger.info(f'Disabling column {column} since it\'s full.')
            self.__drop_row.disable_column(column)

        # Next player is up
        self.__switch_player()

    def __check_four_in_a_row(self, column, row):
        """
        Check whether we have four of the same colour in a row.
        Note that "four in a row" means four adjacent chips of
        the same colour in *any* direction.
        :param column: Column of the location that was played
        :param row: Row of the location that was played
        """
        tu = column, row
        ccol = self.__current_colour

        # Get the list of potential "four in a row"s that may be winner
        fours_to_check = self.__four_in_a_row[tu]
        for four in fours_to_check:
            for c, r in four:
                try:
                    cell_colour = self.__columns[c][r]
                except IndexError:
                    logger.warning('Unused cell')
                    break
                else:
                    if cell_colour != ccol:
                        logger.warning('Wrong colour')
                        break
            else:
                logger.info('Found four in row!')
                return True

        logger.info('No four in a row this time.')
        return False

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
