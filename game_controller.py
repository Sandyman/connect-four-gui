import logging
from random import randint
from time import sleep
from drop_row import DropRow
from four_in_a_row import FourInARow
from game_board import GameBoard

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class GameController:
    COLUMNS = 7
    ROWS = 6

    DARK_GREY = '#505070'

    def __init__(self, drop_row: DropRow, game_board: GameBoard, p1='yellow', p2='red'):
        self.__four_in_a_row = FourInARow(cols=self.COLUMNS, rows=self.ROWS)
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

        # Check to see if we have a winner after this move
        winner = self.__check_four_in_a_row(column, row)
        if winner is not None:
            logger.info('We have a winner!')
            for col in range(self.COLUMNS):
                self.__drop_row.disable_column(col)

            self.__flash_cells(winner, self.__current_colour)

            # TODO: Show message that we have a winner
        else:
            # Disable the column if it's full
            if len(selected_column) == self.ROWS:
                logger.info(f'Disabling column {column} since it\'s full.')
                self.__drop_row.disable_column(column)

            # Next player is up
            self.__switch_player()

    def __flash_cells(self, four, colour):
        """
        Flash cells to indicate where the four in a row was found.
        :param four: The cells that make four in a row
        :param colour: Winning colour
        """
        colours = [colour, self.DARK_GREY]
        ccol = 0

        for _ in range(1, 14):
            for col, row in four:
                self.__game_board.update_cell(col, row, colours[ccol])

            sleep(randint(30, 80) / 1000)
            ccol = 1 - ccol

    def __check_four_in_a_row(self, column, row):
        """
        Check whether we have four of the same colour in a row.
        Note that "four in a row" means four adjacent chips of
        the same colour in *any* direction.
        :param column: Column of the location that was played
        :param row: Row of the location that was played
        :return: None if no winner found, tuple of cells otherwise
        """
        tu = column, row
        ccol = self.__current_colour

        # Get the list of potential "four in a row"s that
        # contain the updated cell
        fours_to_check = self.__four_in_a_row[tu]
        for four in fours_to_check:
            for c, r in four:
                try:
                    cell_colour = self.__columns[c][r]
                except IndexError:
                    logger.warning('Empty cell. Moving on.')
                    break
                else:
                    if cell_colour != ccol:
                        logger.warning('Different colour. Moving on.')
                        break
            else:
                logger.info(f'Found four {ccol} in row!')
                return four

        logger.info('No four in a row this time.')
        return None

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
