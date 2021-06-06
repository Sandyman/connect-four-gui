class Column:
    """
    This class keeps track of a single columns. Such a column
    contains a list of locations that can be played. It provides
    a few handy methods like {next} to provide the next empty
    cell, {is_full} which indicates whether the column is full
    (True) or not (False).
    """
    def __init__(self, size=4):
        self.__size = size
        self.__rows = list()

    def __getitem__(self, item):
        return self.__rows[item]

    @property
    def is_full(self):
        """
        Return True if the column is full, False otherwise.
        """
        return len(self.__rows) == self.__size

    @property
    def next(self):
        """
        Return the next cell that is empty.
        """
        return len(self.__rows)

    def add(self, val):
        """
        Add a value (player's colour?) to the internal list.

        :param val: Value to add to the list
        :return: The position of the row just played
        """
        _next = len(self.__rows)
        self.__rows.append(val)
        return _next
