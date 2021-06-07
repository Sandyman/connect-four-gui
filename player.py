from datetime import datetime


class Player:
    def __init__(self, colour):
        self.__colour = colour

        self.__now = None
        self.__turns = 1
        self.__elapsed_time = 1  # in ms

    @property
    def colour(self):
        return self.__colour

    @property
    def now(self):
        return datetime.now()

    def start_turn(self):
        """
        Start of turn for this player. Update turn count. Store
        current timestamp that will be used to calculate the
        final score for this player.
        """
        self.__turns += 1
        self.__now = self.now

    def end_turn(self):
        """
        End of turn for this player. Update elapsed time.
        """
        if self.__now is not None:
            self.__elapsed_time += round((self.now - self.__now).total_seconds() * 250)

    @property
    def elapsed_time(self):
        return self.__elapsed_time

    def _score(self):
        """
        Calculate the score by multiplying the number of turns
        with the elapsed time in milliseconds. Can be overriden
        if someone wants a different scoring algorithm.

        :return: The score
        """
        return self.__turns * self.elapsed_time

    @property
    def score(self):
        return self._score()
