import string

from request import *
from bag import *
from musicitem import *


class Collection:
    """
    this class represents basic collection of music items
    with no order and repetition
    """
    def __init__(self):
        """
        initializes an empty collection
        """
        self._itemsset = Bag()

    def __getitem__(self, item):
        """
        Args:
             item (str): id of the element that is in the collection
        Returns:
            element in the collection which id is item
        """
        return self._itemsset[item]

    def __contains__(self, item):
        """
        Args:
            item : instance of MusicItem descendant or string,
                returned by id() method applied to item

        Returns:
            True if item or its id (method id() of MusicItem class)
                is in the collection,
            False otherwise
        """
        return item in self._itemsset

    def add(self, item):
        """
        Adds item to a collection

        Args:
             item : instance of MusicItem descendant
        """
        self._itemsset.add(item)

    def __iter__(self):
        """
        Returns:
            iterator for items in a collection
        """
        return self._itemsset.__iter__()

    def pythoncode(self):
        """
        Returns:
             generator for python representation of
             all items in a collection
        """
        for item in self:
            yield repr(item)

    @classmethod
    def process_from_file(cls, file, itemclass, printinfo=False):
        """
        returns Collection instance
        with given descendant class,
        items file and one of MusicItem descendant classes
        that correspond to cls

        see Collection.pythoncode() for more details

        Args:
             file : file opened for reading
             itemclass : class of items of the collection
             printinfo (bool): if True, show information about
                already processed items while working
        Returns:
            new Collection descendant instance
        """
        tempcollection = cls()
        counter = 0
        print('\nLoading %ss\n' % (itemclass.__name__))
        for line in file:
            line = line.strip()
            if line != '':
                counter += 1
                if printinfo:
                    print('\r' + "Loading (DO NOT QUIT!!!)" + str(counter),
                          end='')
                tempitem = itemclass.process_from_file(eval(line))
                tempcollection.add(tempitem)
        if printinfo:
            print()
        return tempcollection


class ArtistCollection(Collection):
    """
    this class represents more specific information
    about ArtistCollection
    """
    @classmethod
    def process_from_file(cls, file, printinfo=False):
        return super().process_from_file(file, Artist, printinfo)


class AlbumCollection(Collection):
    """
    this class represents more specific information
    about AlbumCollection
    """
    @classmethod
    def process_from_file(cls, file, printinfo=False):
        return super().process_from_file(file, Album, printinfo)


class SongCollection(Collection):
    """
    this class represents more specific information
    about SongCollection
    """
    @classmethod
    def process_from_file(cls, file, printinfo=False):
        return super().process_from_file(file, Song, printinfo)


class FeatureCollection(Collection):
    """
    this class represents more specific information
    about FeatureCollection
    """
    @classmethod
    def process_from_file(cls, file, printinfo=False):
        return super().process_from_file(file, Feature, printinfo)