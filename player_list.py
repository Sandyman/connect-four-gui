class _PlayerItem:
    """
    This class is the data structure that holds the player
    information and a reference to the next Player Item.
    """

    def __init__(self, item):
        self.item = item
        self.next = None


class PlayerList:
    """
    This class holds a list of player. It's a linked list, so
    it's relatively straightforward to get the "next" player.
    We implement an iterator for that purpose.
    """
    def __init__(self, *players):
        self.__first = None
        self.__last = None
        self.__current = None

        for player in players:
            self.add(player)

    def __iter__(self):
        self.__current = self.__first
        return self

    def __next__(self):
        if self.__current is not None:
            current = self.__current
            self.__current = current.next
            return current.item
        else:
            raise StopIteration

    def add(self, player):
        """
        Add a new player to the list. Creates a PlayerItem and
        updates the internal references.

        :param player: Player to add
        """
        player_item = _PlayerItem(player)
        if self.__first is None:
            self.__first = player_item
        else:
            self.__last.next = player_item

        self.__last = player_item
        player_item.next = self.__first
