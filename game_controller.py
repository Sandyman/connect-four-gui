import logging
from random import randint
from time import sleep
from column import Column
from drop_row import DropRow
from four_in_a_row import FourInARow
from game_board import GameBoard
from player import Player
from player_list import PlayerList

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

        # Create player list and easy way to move through player turns (iterate)
        players = PlayerList(Player(p1), Player(p2))
        self.__players = iter(players)
        self.__current_player = next(self.__players)

        self.__drop_row.set_active_colour(self.__current_colour)

        drop_row.set_click_handler(self.__column_clicked)

        self.__columns = [Column(size=self.ROWS) for _ in range(self.COLUMNS)]

    @property
    def __current_colour(self):
        """
        Get the current colour based on the current player
        :return: Colour for current player
        """
        return self.__current_player.colour

    @staticmethod
    def __row(row):
        """
        This basically flips the coordinates vertically:

            0 -> 5, 1 -> 4, ... 5 -> 0

        :param row: Row to translate (mirror)
        """
        return GameController.ROWS - 1 - row

    def __column_clicked(self, column):
        logger.info(f'Column {column} clicked!')

        selected_column = self.__columns[column]
        if selected_column.is_full:
            logger.warning(f'Column {column} is full!')
            return

        # Add current player's colour and retrieve row it was placed in
        row = selected_column.add(self.__current_colour)

        logger.info(f'Valid move: (col,row)=({column},{row})')

        # Update the cell on the board
        self.__game_board.update_cell(column, self.__row(row), self.__current_colour)

        # Check to see if we have a winner after this move
        winning_four = self.__check_four_in_a_row(column, row)
        if winning_four is not None:
            logger.info('We have a winner!')

            # Disable all columns at once
            self.__drop_row.disable_column(column=None)

            # Visual indication of the winning row
            self.__flash_cells(winning_four, self.__current_colour)

            # TODO: Show message that we have a winner
        else:
            # Disable the column if it's full
            if selected_column.is_full:
                logger.info(f'Disabling column {column} since it\'s full.')
                self.__drop_row.disable_column(column)

            # Next player is up
            self.__next_player()

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
                self.__game_board.update_cell(col, self.__row(row), colours[ccol])

            # Wait for a really short time
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
        cols = self.__columns
        ccol = self.__current_colour

        # Get the list of potential "four in a row"s that
        # contain the updated cell
        fours_to_check = self.__four_in_a_row[tu]
        for four in fours_to_check:
            try:
                row = list(filter(lambda x: cols[x[0]][x[1]] == ccol, four))
            except IndexError:
                logger.warning('Empty cell encountered. Moving on.')
                continue
            else:
                if len(row) == 4:
                    logger.info(f'Found four {ccol} in row!')
                    return four

        logger.info('No four in a row this time.')
        return None

    def __next_player(self):
        """
        Switch player. This also switches the colour for convenience.
        """
        self.__current_player = next(self.__players)
        self.__drop_row.set_active_colour(self.__current_colour)
