from functools import reduce


class FourInARow:
    """
    This class build a data structure containing all possible
    "four in a rows" and maps them to individual cells. That
    way, we can simply ask for all possible combinations that
    need to be checked for "four in a row" that contains the
    individual cell. For example, if the updated cell is (0,0),
    which is the bottom-left cell, then we only need to check
    three "four in a rows"s: one horizontal, one vertical, and
    one diagonal.

    This class makes the index operator available. The key for
    it is a (column, row)-tuple, for example (4, 3). No validation
    takes place; if the provided key does not exist, a KeyError
    will be raised.

    The index operator returns a list of tuples of tuples, for
    example:

    (0, 0) => [
        ((0, 0), (1, 0), (2, 0), (3, 0)),  # horizontal
        ((0, 0), (1, 1), (2, 2), (3, 3)),  # diagonal
        ((0, 0), (0, 1), (0, 2), (0, 3)),  # vertical
    ]

    where each tuple contains four tuples of the form (col, row).
    """
    def __init__(self, cols, rows):
        # Seems harsh, but it is called FourInARow...
        assert cols >= 4 and rows >= 4

        self.__columns = cols
        self.__rows = rows

        # Get all possible "four in a row"s in all directions
        fours = list()
        fours.extend(self.__get_horizontal_fours())
        fours.extend(self.__get_vertical_fours())
        fours.extend(self.__get_diagonal_fours())

        # Map all possible "four in a row"s to individual cells
        self.__fours_map = self.__map_fours(fours)

    def __getitem__(self, key):
        """
        Return the list of "four in a row"s for a certain cell.
        :param key: A single (col,row)-tuple
        :return: A list of tuples containing exactly four (col,row)-tuples
        """
        return self.__fours_map[key]

    def __map_fours(self, fours):
        """
        Map each of the "four in a row"s to the cells that they
        contain to create a dictionary of "four in a row"s. The
        key, therefore, is a cell which points to a list of
        "four in a row"s that could possibly be made when that
        cell is updated.
        """
        def st(acc, key):
            """
            Create a list of "four in a row"s that contain the cell {key}
            :param acc: Accumulator (dictionary) to update
            :param key: The value to use as key and as filtering item
            :return: Updated accumulator
            """
            acc[key] = list(filter(lambda z: key in z, fours))
            return acc

        # Get a list of all cells as (col,row)-tuples
        all_cells = [(col, row)
                     for col in range(self.__columns)
                     for row in range(self.__rows)
                     ]

        return reduce(st, all_cells, {})

    def __get_horizontal_fours(self):
        """
        Get all the possible horizontal "four in a row"s.
        """
        cols, rows = self.__columns, self.__rows
        return [
            tuple((col + i, row) for i in range(4)) for col in range(cols - 3) for row in range(rows)
        ]

    def __get_vertical_fours(self):
        """
        Get all the possible vertical "four in a row"s.
        """
        cols, rows = self.__columns, self.__rows
        return [
            tuple((col, row + i) for i in range(4)) for col in range(cols) for row in range(rows - 3)
        ]

    def __get_diagonal_fours(self):
        """
        Get all the possible diagonal "four in a row"s.
        """
        cols, rows = self.__columns, self.__rows
        diagonals = list()
        for col in range(cols - 3):
            for row in range(rows - 3):
                diagonals.append(tuple((col + i, row + i) for i in range(4)))
                diagonals.append(tuple((cols - (col + i + 1), row + i) for i in range(4)))

        return diagonals


def main():
    cols = 7
    rows = 6
    fiar = FourInARow(cols, rows)

    for col in range(cols):
        for row in range(rows):
            tu = col, row
            print(f'{tu} => {fiar[tu]}')


if __name__ == '__main__':
    main()
