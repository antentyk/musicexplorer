class SearchRequest:
    """
    this class represents a search request
    with search query and offset
    """
    def __init__(self, q='a', offset=0):
        """
        Initializes new SearchRequest instance
        with given arguments

        Args:
            q (str): search query for the request
            offset (int): query offset
        """
        self._q = q
        self._offset = offset

    def __getitem__(self, item):
        """
        Args:
             item (str): name of the attribute
                that you need to access
        Returns:
            attribute of self, which is named item
            if there is no such an attribute, KeyError is raised
        """
        if item == 'q':
            return self._q
        if item == 'offset':
            return self._offset
        raise KeyError

    def __setitem__(self, key, value):
        """
        tries to set key attribute to value
        if there is no such an attribute,
        KeyError is raised

        Args:
            key (str): name of the attribute that you want
                to change
            value (str): new value, that you want to set
        """
        if key == 'q':
            self._q = value
            return None
        if key == 'offset':
            self._offset = value
            return None
        raise KeyError

    def __repr__(self):
        """
        Returns:
            str - python representation of the tuple,
                that contains information about the request
        """
        return "request = ('%s', %s)" % (self['q'], self['offset'])

    @staticmethod
    def process_from_file(item):
        """
        Args:
             item (tuple): representation of the request
             (see __repr__ documentation)
        Returns:
            new SearchRequest instance
        """
        return SearchRequest(item[0], item[1])


class GetRequest:
    """
    This class represents get request
    """

    def __init__(self, n=0):
        """
        Initializes new GetRequest instance with given n

        Args:
            n (int): number of items of the sequence,
                that have already beed analyzed
        """
        self._n = n

    def __getitem__(self, item):
        """
        Returns:
             item attribute of self
             if there is no such an attribute,
             KeyError is raised
        """
        if item == 'n':
            return self._n
        raise KeyError

    def __setitem__(self, key, value):
        """
        Args:
             key (str): attribute, that you want to change
             value (int): new value of an attribute that you want to set

        if there is no such an attribute,
            KeyError is raised
        """
        if key == 'n':
            self._n = value
            return None
        raise KeyError

    def __repr__(self):
        """
        Returns:
             str - python representation of a tuple,
                that contains information about the request
        """
        return "request = (%s,)" % self['n']

    @staticmethod
    def process_from_file(item):
        """
        Returns new GetRequest instance with information,
        given in item

        Args:
            item (tuple): python representation of the request
                (see __repr__ documentation)

        Returns:
            new GetRequest instance
        """
        return GetRequest(item[0])
