class SimpleBag:
    """
    This class represents bag of
    instances with no order and repetition
    """

    def __init__(self):
        """
        Initializes an empty bag
        """
        self._items = set()

    def get_length(self):
        """
        Returns:
             number of items in the bag
        """
        return len(self._items)

    def add(self, item):
        """
        Adds item to a bag

        Args:
            item: class instance that needs
                to be added to the bag
        """
        self._items.add(item)

    def __iter__(self):
        """
        Returns:
             iterator for items in the bag
        """
        return self._items.__iter__()

    def __contains__(self, item):
        """
        Returns:
             True if item is in tha bag,
             False otherwise
        """
        return item in self._items


class Bag:
    """
    This class represents more complex
    bag that stores instance that
    has id() method, that should return string

    The values are stored with
    no order and repetition

    You should use return value of id() method
    to access elements in the bag
    """

    def __init__(self):
        """
        Initializes an empty bag
        """
        self._items = {}

    def get_length(self):
        """
        Returns:
             number of items in the bag
        """
        return len(self._items)

    def add(self, item):
        """
        Adds item to the bag
        if there is already something with the same
        id, rewrites it

        Precognition: item should have
            id() method that returns string

        Args:
            item: class instance that needs
                to be added to the bag
        """
        self._items[item.id()] = item

    def __contains__(self, item):
        """
        Args:
            item (str or class instance): item that will be
                checked for entry in the bag

        Returns:
            True if item is in the bag.
            False otherwise
        """
        if isinstance(item, str):
            return item in self._items
        else:
            return item in self._items.values()

    def __getitem__(self, key):
        """
        Args:
            key(str): key of the item in the bag
                (return value of id() method)
        Returns:
            item in a bag for given key

        if key has wrong type or there is not
        such a key in the bag,
        KeyError is raised
        """
        if isinstance(key, str):
            return self._items[key]
        raise KeyError

    def __iter__(self):
        """
        Returns:
             generator for items in the bag
        """
        for i in self._items:
            yield self._items[i]