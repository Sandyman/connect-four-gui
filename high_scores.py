from functools import reduce


class HighScores:
    """
    A class that stores high scores as (score, initials)-tuple,
    for example, (32412, 'ah ').

    This class assumes that "high" scores are actually lower
    score values. High, in this occasion, therefore means
    better.
    """

    def __init__(self, count=10):
        self.__max_scores = count
        self.__high_scores = list()

    def is_high_score(self, score):
        """
        Determine whether {score} is a high score. Note that
        this class has an inverse high score: a "high" score
        is, in fact, a low score. That's why the list is
        sorted in ascending order.
        :param score:
        :return:
        """
        return not self.__high_scores or score <= self.__high_scores[-1][0]

    def add_high_score(self, score, initials):
        """
        Add high scores to the high score table. If a score is
        added that equals an existing score, then the new
        score takes precedence over the old score.

        :param score: The score to store
        :param initials: Initials of the high score owner
        """
        high_scores = self.__high_scores
        indx = self.__index(score)
        high_scores.insert(indx, (score, initials))
        self.__high_scores = high_scores[:self.__max_scores]

    def __index(self, score):
        """
        Calculate the index of the high score (which may be
        beyond the end of the current high scores).
        :param score: Score to find in the list of high scores
        :return: The index where this score would go
        """
        return reduce(lambda x, y: x if y[0] >= score else x + 1,
                      self.__high_scores,
                      0)

    @property
    def high_scores(self):
        """
        This returns a copy of the high score list.
        :return: List with high scores - a copy of the original
        """
        return self.__high_scores.copy()
