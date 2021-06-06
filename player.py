class Player:
    def __init__(self, colour):
        self.__colour = colour

    @property
    def colour(self):
        return self.__colour
