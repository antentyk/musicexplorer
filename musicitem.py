from bag import *


class MusicItem:
    """
    This class represents basic music item
    with spotify id and popularity
    """

    def __init__(self, id, popularity):
        """
        Initializes MusicItem instance with
            given id and popularity

        Args:
            id(str): spotify id of the item
            popularity(int): popularity of the item
        """
        self._id = id
        self._popularity = popularity

    def id(self):
        """
        Returns:
             id of the item
        """
        return self._id

    def popularity(self):
        """
        Returns:
             popularity of the item
        """
        return self._popularity


class Artist(MusicItem):
    """
    This class provides with more specific
    information about an artist
    """

    def __init__(self, id, name, popularity):
        """
        Initializes new Artist instance with
        given id, name and popularity

        Args:
            id(str): Spotify id of the song
            name(str): name of the artist
            popularity(int): overall popularity of an artist
        """
        super().__init__(id, popularity)
        self._name = name.replace('"', "'")

    def name(self):
        """
        Returns:
             name of an Artist
        """
        return self._name

    def __eq__(self, other):
        """
        Args:
             other: another instance of Artist class
        Returns:
            True if id of self is equal to id of other,
            False otherwise
        """
        return self.id() == other.id()

    def __hash__(self):
        """
        Returns:
            hash of self as hash of its id
        """
        return hash(self.id())

    def __repr__(self):
        """
        Returns:
             str - representation of Python
                tuple with id, name and popularity
                of self
        """
        return """("%s", "%s", %s)""" % (self.id(),
                                         self.name(),
                                         str(self.popularity()))

    @staticmethod
    def process_from_file(item):
        """
        returns new Artist instance,
        information is taken from item tuple

        Args:
            item (tuple(str, str, int)): tuple representation
                of an artist(id, name popularity)
        Returns:
            Artist instance
        """
        return Artist(item[0], item[1], item[2])

    @staticmethod
    def process_from_request(artistfull):
        """
        returns new Artist instance,
        information is taken from artistfull

        Args:
            artistfull (dict): Spotify ArtistFull object
            visit https://developer.spotify.com/
                  web-api/object-model/#artist-object-full
            for more information
        Returns:
            Artist instance
        """
        return Artist(artistfull["id"],
                      artistfull["name"],
                      artistfull["popularity"])


class Album(MusicItem):
    """
    This class provides with more specific
    information about an album
    """

    def __init__(self,
                 id,
                 name,
                 release_date,
                 popularity,
                 artists,
                 songs):
        """
        initializes new Album with given
        arguments

        Args:
            id (str): Spotify id of the album
            name (str): name of the album
            release_date (tuple): tuple of ints that represents
                release date. It can be year and month
                or just year
            popularity (int): popularity of the album
            artists (list(str)): list of ids of artists,
                who preformed in the album
            songs (list(str)): list of ids of songs inthe album
        """
        super().__init__(id, popularity)
        self._songs = SimpleBag()
        for item in songs:
            self._songs.add(item)
        self._artists = SimpleBag()
        for item in artists:
            self._artists.add(item)
        self._release_date = release_date
        self._name = name.replace('"', "'")


    def songs(self):
        """
        Returns:
             iterator for songs in the album
        """
        return self._songs.__iter__()

    def artist(self):
        """
        Returns:
            iterator for artists in the album
        """
        return self._artists.__iter__()

    def addsong(self, value):
        """
        adds song to the album

        Args:
             value (str): spotify id of the song

        """
        self._songs.add(value)

    def addartist(self, value):
        """
        adds artist to the album
        """
        self._artists.add(value)

    def name(self):
        """
        Returns:
             name of the album
        """
        return self._name

    def release_date(self):
        """
        Returns:
             release date of the album
        """
        return self._release_date

    def __eq__(self, other):
        """
        Args:
             other : another instance of Album class
        Returns:
            True, if id of self and other are the same,
            False otherwise
        """
        return self.id() == other.id()

    def __hash__(self):
        """
        Returns:
             hash of self as hash of its id
        """
        return hash(self.id())

    def __repr__(self):
        """
        Returns:
            str - python representation of the tuple
                with information about the album
                (id, name, release date, popularity, artists and songs)
        """
        return """("%s", "%s", %s, %s, %s, %s)""" \
               % (self.id(),
                  self.name(),
                  str(self.release_date()),
                  str(self.popularity()),
                  '[' +
                  ','.join(('"' + item + '"' for item in self._artists)) +
                  ']',
                  '[' + ','.join(('"' + item + '"' for item in self._songs)) +
                  ']')

    @staticmethod
    def process_from_request(albumfull):
        """
        Returns new Album instance with information,
        given in request

        Args:
             albumfull (dict): Spotify album full object
             see https://developer.spotify.com/
                 web-api/object-model/#album-object-full
             for more details

        Returns:
            new Album instance
        """
        artists = SimpleBag()
        for item in albumfull["artists"]:
            artists.add(item["id"])
        songs = SimpleBag()
        for item in albumfull["tracks"]["items"]:
            songs.add(item["id"])
        return Album(albumfull["id"],
                     albumfull["name"],
                     Album.process_release_date(albumfull),
                     albumfull["popularity"],
                     artists,
                     songs)

    @staticmethod
    def process_release_date(albumfull):
        """
        Returns release date in appropriate format
        from album information

        Args:
            albumfull (dict): Spotify album full object
            see https://developer.spotify.com/
                 web-api/object-model/#album-object-full
             for more details

        Returns:
            tuple of integers (year and month of release)
            (it also can be just year)
        """
        precision = albumfull["release_date_precision"]
        date = albumfull["release_date"]
        if precision == "year":
            return (int(date),)
        if precision == "month":
            return tuple(map(int, date.split('-')))
        return tuple(map(int, date.split('-')[:-1]))

    @staticmethod
    def process_from_file(item):
        """
        Args:
            item (tuple): tuple represenation of the album
            (see __repr__ documentation)
        Returns:
            new Album instance
        """
        return Album(item[0],
                     item[1],
                     item[2],
                     item[3],
                     item[4],
                     item[5])


class Song(MusicItem):
    """
    This class provides with
    more specific information
    about song
    """
    def __init__(self,
                 id,
                 albumid,
                 popularity):
        """
        Initializes new Song instance with
        given values

        Args:
            id (str): Spotify id of the song
            albumid (str): Spotify id of the album,
                that contains this song
            popularity (int): popularity of this song
        """
        super().__init__(id, popularity)
        self._albumid = albumid

    def __gt__(self, other):
        """
        Compares popularity of self song and other song
        Returns:
            True if popularity of self is greater that
                popularity of other
            False otherwise
        Args:
            self (Song)
            other (Song)
        """
        return self.popularity() > other.popularity()

    def __lt__(self, other):
        """
        Compares popularity of self song and other song
        Returns:
            True if popularity of self is less that
                popularity of other
            False otherwise
        Args:
            self (Song)
            other (Song)
        """
        return self.popularity() < other.popularity()

    def __eq__(self, other):
        """
        Compares popularity of self song and other song
        Returns:
            True if popularity of self is equal to
                popularity of other
            False otherwise
        Args:
            self (Song)
            other (Song)
        """
        return self.popularity() == other.popularity()

    def __le__(self, other):
        """
        see Song.__eq__() and Song.__lt__()
        documentation for more detail
        """
        return self < other or self == other

    def __ge__(self, other):
        """
        see Song.__eq__() and Song.__gt__()
        documentation for more detail
        """
        return self > other or self == other

    def albumid(self):
        """
        Returns:
             str - id of the album, that contains the song
        """
        return self._albumid

    def __repr__(self):
        """
        Returns:
             str - python representation of the tuple
                with information about a song
        """
        return "('%s', '%s', %s)" % (self.id(),
                                     self.albumid(),
                                     self.popularity())

    @staticmethod
    def process_from_file(item):
        """
        Args:
            item (tuple): representation of the song
            (see __repr__ documentation)

        Returns:
             new Song instance
        """
        return Song(item[0], item[1], item[2])

    @staticmethod
    def process(songfull):
        """
        Args:
            songfull (dict): Spotify track full object
                see https://developer.spotify.com/
                    web-api/object-model/#track-object-full
                for more information

        Returns:
             new Song instance
        """
        return Song(songfull["id"],
                    songfull["album"]["id"],
                    songfull["popularity"])


class Feature(MusicItem):
    """
    This class provides with more specific information
    about song features
    """

    # setting list of attributes of the class
    ATTRS = ['id',
             'acousticness',
             'danceability',
             'duration_ms',
             'energy',
             'instrumentalness',
             'key',
             'loudness',
             'mode',
             'speechiness',
             'tempo',
             'time_signature',
             'valence']

    def __init__(self,
                 id=0,
                 acousticness=0,
                 danceability=0,
                 duration_ms=0,
                 energy=0,
                 instrumentalness=0,
                 key=0,
                 loudness=0,
                 mode=0,
                 speechiness=0,
                 tempo=0,
                 time_signature=0,
                 valence=0):
        """
        Initializes new Feature instance with
        given arguments

        id (str): id of the song, that is being analyzed
        acousticness (float)
        danceability (float)
        duration_ms (int)
        energy (float)
        instrumentalness (int)
        key (int) - (C - 0, C# - 1, D - 2 etc.)
        loudness (int): loudness of the track in db
        mode (int): 1 - major, 0 - minor
        speechiness (float): detects the presence of spoken words in a track
        tempo (int): bpm
        time_signature (int): The time signature (meter) is a
                              notational convention
                              to specify how many beats are in each bar
        valence (float): musical positiveness conveyed by a track
        """
        self._id = id
        self._acousticness = acousticness
        self._danceability = danceability
        self._duration_ms = duration_ms
        self._energy = energy
        self._instrumentalness = instrumentalness
        self._key = key
        self._loudness = loudness
        self._mode = mode
        self._speechiness = speechiness
        self._tempo = tempo
        self._time_signature = time_signature
        self._valence = valence

    def __setitem__(self, key, value):
        """
        Tries to change key attribute to value
        if there is no such an attribute, KeyError is raised
        if value has wrong type, TypeError is raised
        Args:
             key (str): name of an attribute that needs to be changed
             value (int or float): new value of the attribute
        """
        if not (isinstance(value, int) or isinstance(value, float)):
            raise TypeError
        if key not in self.ATTRS[1:]:
            raise KeyError
        exec("self._%s = %s" % (key, value))


    def popularity(self):
        raise NotImplementedError

    def __getitem__(self, item):
        """
        Args:
             item (str): name of the attribute
                that you need to access
        Returns:
            item attribute of the feature
            if there is not such an attribute,
            KeyError is raised
        """
        if item not in self.ATTRS:
            raise KeyError
        else:
            return eval('self._' + item)

    def __repr__(self):
        """
        Returns:
             str - python representation of a tuple
             with information about a feature
        """
        return ("(" +
                ("'%s'," % self['id']) +
                ','.join(map(str, [self[item] for item in self.ATTRS[1:]])) +
                ")")

    def check(self):
        """
        checks if all the attributes do not have None value
        Returns:
            False, if even one of the arguments is None,
            True otherwise
        """
        for item in self.ATTRS:
            if self[item] is None:
                return False
        return True

    @staticmethod
    def process_from_file(item):
        """
        Args:
             item (tuple): tuple representation of the
                feature (see __repr__ documentation)
        Returns:
            new Feature instance
        """
        return Feature(item[0],
                       item[1],
                       item[2],
                       item[3],
                       item[4],
                       item[5],
                       item[6],
                       item[7],
                       item[8],
                       item[9],
                       item[10],
                       item[11],
                       item[12])

    @classmethod
    def process(cls, featuresfull):
        """
        returns new Feature instance from
        features spotify object

        Args:
            featuresfull (dict): spotify features object
                see https://developer.spotify.com/
                web-api/object-model/#audio-features-object
                for more information
        Returns:
             new Feature instance
        """
        return Feature(featuresfull['id'],
                       featuresfull['acousticness'],
                       featuresfull['danceability'],
                       featuresfull['duration_ms'],
                       featuresfull['energy'],
                       featuresfull['instrumentalness'],
                       featuresfull['key'],
                       featuresfull['loudness'],
                       featuresfull['mode'],
                       featuresfull['speechiness'],
                       featuresfull['tempo'],
                       featuresfull['time_signature'],
                       featuresfull['valence'])
