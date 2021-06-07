import logging
from random import randint
from time import sleep
from column import Column
from drop_row import DropRow
from four_in_a_row import FourInARow
from game_board import GameBoard

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class GameController:
    DARK_GREY = '#505070'

    def __init__(self, parent, drop_row: DropRow, game_board: GameBoard,
                 players, columns, rows):
        self.__parent = parent
        self.__columns = columns
        self.__rows = rows

        self.__active_columns = set(range(columns))

        self.__four_in_a_row = FourInARow(columns, rows)
        self.__drop_row = drop_row
        self.__game_board = game_board

        # The players object is an iterable
        self.__players = players
        self.__current_player = next(self.__players)

        # Set active colour for drop row to current player's colour
        self.__drop_row.set_active_colour(self.__current_colour)

        # Create columns and set click handler for the drop row
        self.__columns = [Column(size=rows) for _ in range(columns)]
        drop_row.set_click_handler(self.__column_clicked)

        # Start turn for first player
        self.__current_player.start_turn()

    @property
    def __current_colour(self):
        """
        Get the current colour based on the current player
        :return: Colour for current player
        """
        return self.__current_player.colour

    def __row(self, row):
        """
        This basically flips the coordinates vertically:

            0 -> 5, 1 -> 4, ... 5 -> 0

        :param row: Row to translate (mirror)
        """
        return self.__rows - 1 - row

    def __column_clicked(self, column):
        logger.info(f'Column {column} clicked!')

        # End the player's turn (stop the time)
        self.__current_player.end_turn()

        # Check that clicked column isn't already full
        selected_column = self.__columns[column]
        if selected_column.is_full:
            logger.warning(f'Column {column} is full! - This should not happen.')
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

            # Disable all column before showing the winning row
            self.__drop_row.disable_column(column=None)

            # Visual indication of the winning row
            self.__flash_cells(winning_four, self.__current_colour)

            logger.info(f'The winner scored {self.__current_player.score} points')

            # Disable all column and inform parent that it's game over
            self.__parent.game_over(self.__current_player)
        else:
            if selected_column.is_full:
                logger.info(f'Disabling column {column} since it\'s full.')

                # Disable the column because it's full
                self.__disable_column(column)

                # Check whether the whole board is full (game over if so)
                if self.__is_board_full():
                    logger.info("The whole board is full. So, it's a tie.")

                    self.__drop_row.disable_column(column=None)
                    self.__parent.game_over(None)
                    return

            # Next player is up
            self.__next_player()
            self.__current_player.start_turn()

    def __disable_column(self, column):
        """
        Disable a column. Update the set of disabled columns.

        :param column: Column to disable
        :return:
        """
        self.__drop_row.disable_column(column)
        self.__active_columns.remove(column)

    def __is_board_full(self):
        """
        Return True if the board is full, False otherwise
        """
        return not self.__active_columns

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
                self.__game_board.update_cell(col, self.__row(row),
                                              colour=colours[ccol],
                                              update_now=True)

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
