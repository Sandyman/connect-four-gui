from functools import reduce


class HighScores:
    """
    A class that stores high scores as (score, initials)-tuple,
    for example:

        [(32412, 'ahj'), (45129, 'baz'), (59092, 'zhg')]

    This class assumes that "high" scores are actually lower
    score values. High, in this occasion, therefore means
    better.

    Please note that this class does not enfore the use of
    initials, so it's possible to store names in stead of
    initials.
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

        :param score: Score to check against high scores
        :return: True if new score is a high score, False otherwise
        """
        if not self.__high_scores:
            return True
        else:
            worst_high_score = self.__high_scores[-1][0]
            return score <= worst_high_score

    def add_high_score(self, score, initials):
        """
        Add high scores to the high score table. If a score is
        added that equals an existing score, then the new
        score takes precedence over the old score. If it's not
        a high score at all, it will ultimately be discarded.

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
        beyond the end of the current high scores). If the
        exact score already exists, the new score will be
        placed before it. Thus, new high scores beat older
        high scores.

        :param score: Score for which to find the index
        :return: The index where this score would go
        """
        return reduce(lambda x, y: x if y[0] >= score else x + 1,
                      self.__high_scores,
                      0)

    @property
    def high_scores(self):
        """
        This returns a !copy! of the high score list.

        :return: A copy of the high scores list
        """
        return self.__high_scores.copy()


def main():
    h = HighScores(count=2)

    assert h.is_high_score(10) is True

    h.add_high_score(10, 'agb')
    h.add_high_score(20, 'bzd')

    assert h.is_high_score(20) is True
    assert h.is_high_score(21) is False

    h.add_high_score(25, 'gdx')
    print(h.high_scores)
    assert h.high_scores[-1][1] == 'bzd'

    h.add_high_score(20, 'gdx')
    print(h.high_scores)
    assert h.high_scores[-1][1] == 'gdx'

    h.add_high_score(10, 'ief')
    print(h.high_scores)
    assert h.high_scores[0][1] == 'ief'


if __name__ == '__main__':
    main()
