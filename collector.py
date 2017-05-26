import os
import time
import importlib


import spotipy


from collection import *
from request import *
from musicitem import *


class Collector:
    """
    This class represents basic information
    about a collector that stores data
    with no order and repetitions
    """
    def __init__(self, client=spotipy.Spotify()):
        """
        Args:
            client : spotipy Spotify client with right credentials
        """
        self._client = client

    def add(self, item):
        """
        Args:
             item : instance of the class,
                that will be added to a Collector

        Adds item to a collector
        """
        self._items.add(item)

    def __contains__(self, item):
        """
        Args:
             item : instance of the class,
                that will be checked for presence
                in a collection

        Returns:
            True if item is in a collector,
            False otherwise
        """
        return item in self['items']

    def __getitem__(self, item):
        """
        Tries to get an attribute of a collector with
        name item

        Args:
            item (str): name of an atribute

        Returns:
            attribute of the collector

        If there is not such an attribute,
        KeyError is raised
        """
        if item == 'request':
            return self._request
        if item == 'client':
            return self._client
        if item == 'items':
            return self._items
        raise KeyError

    def __iter__(self):
        """
        Returns:
             iterator for items in a collector
        """
        return self['items'].__iter__()

    def save(self, foldername, printinfo=False):
        """
        Saves currently avalilable information
        about the music items in the collector
        into self.FILESDIR/foldername directory

        Args:
             foldername (str): name of the folder inside
                self.FILESDIR, where data about collected
                music items will be stored
             printinfo (bool): if True, show information about
                already saved music items while working
        """
        self.prepare_dir()
        counter = 0
        print("\nSaving\n")
        path = self.FILESDIR + '/' + foldername

        if not os.path.isdir(path):
            os.mkdir(path)

        itemsfile = open(path + '/items.txt', 'w', encoding='utf8')
        requestfile = open(path + '/request.py', 'w', encoding='utf8')

        for line in self['items'].pythoncode():
            counter += 1
            if printinfo:
                print("\r" + "SAVING DO NOT QUIT " + str(counter), end='')
            itemsfile.write(line + '\n')

        requestfile.write(repr(self['request']))

        itemsfile.close()
        requestfile.close()

    def load(self,
             foldername,
             requestclass,
             collectionclass,
             printinfo=False):
        """
        Tries to load saved information about already collected
        music items

        Args:
            foldername (str): name of the folder inside
                self.FILESDIR, where data is stored
            requestclass : class of the request
                (GetRequest or SearchRequest)
            collectionclass : class of collection that is
                used in Collector instance
                (ArtistCollection or AlbumCollection)
            printinfo (bool): if True, show information about
                already loaded music items while working
        """
        try:
            requestmodule = importlib.import_module("%s.%s.request" %
                                                    (self.FILESDIR,
                                                     foldername))
            self._request = requestclass.process_from_file\
                (requestmodule.request)

            itemsfile = open("%s/%s/items.txt" % (self.FILESDIR, foldername),
                             'r', encoding='utf8')
            self._items = collectionclass.process_from_file(itemsfile,
                                                            printinfo)
        except:
            pass

    @classmethod
    def prepare_dir(cls):
        """
        Checks if folder with collector files exists
        If not, creates this folder
        """
        if not os.path.isdir(cls.FILESDIR):
            os.mkdir(cls.FILESDIR)


class ArtistCollector(Collector):
    """
    This class represents specific information
    about Artist collector
    """


    # setting constants
    SEARCHLETTERS = string.ascii_lowercase
    QUERYLIMIT = 50
    FILESDIR = 'artistfiles'
    MAXOFFSET = 100000


    def __init__(self, client=spotipy.Spotify()):
        """
        Initializes new ArtistCollector instance

        Args:
            client : spotipy Spotify client with right credentials
        """
        super().__init__(client)
        self._request = SearchRequest()
        self._items = ArtistCollection()

    def get(self, limit=float('inf'), lowestpopularity=0):
        """
        Tries to get some artists with popularity that is
        higher than lowestpopularity

        Args:
            limit (int): maximal number of artists,
                that should be analyzed
            lowestpopularity (int): lowest popularity of the artists,
                that will be added to a collector
        """
        assert(isinstance(limit, int) or isinstance(limit, float))
        assert(isinstance(lowestpopularity, int))
        try:
            self._get(limit, lowestpopularity)
        except:
            pass

    def _get(self, limit, lowestpopularity):
        """
        Helper method to get artists
        """
        print("\nCollecting\n")
        firsttime = True
        overallcounter = 0
        firstletterindex = self.\
            SEARCHLETTERS.index(self['request']['q'].lower())

        for letter in self.SEARCHLETTERS[firstletterindex:]:
            if overallcounter >= limit:
                break

            self['request']['q'] = letter
            q = letter + '*'

            if firsttime:
                firsttime = False
                offset = self['request']['offset']
            else:
                offset = 0
                self['request']['offset'] = 0

            lowpopularity = False
            result = self['client'].search(type='artist',
                                           q=q,
                                           offset=offset,
                                           limit=self.QUERYLIMIT)

            while (overallcounter < limit and
                   not lowpopularity and
                   result['artists']['items'] and
                   self['request']['offset'] < self.MAXOFFSET):
                for item in result['artists']['items']:
                    tempartist = Artist.process_from_request(item)

                    if tempartist.popularity() <= lowestpopularity:
                        lowpopularity = True
                        break

                    self.add(tempartist)
                    overallcounter += 1
                    self['request']['offset'] += 1

                print('\r' + "COLLECTING DATA " + str(overallcounter) , end='')
                if overallcounter >= limit:
                    break

                result = self['client'].next(result['artists'])

    def load(self, foldername, printinfo=False):
        """
        Loads information abot artists
        from self.FILESDIR/foldername directory

        Args:
            foldername (str): name of the folder inside self.FILESDIR
                where data is stored
            printinfo (bool): if True, show information about
                already loaded artists while working
        """
        super().load(foldername,
                     SearchRequest,
                     ArtistCollection,
                     printinfo)


class AlbumCollector(Collector):
    """
    This class represents more specific information about
    AlbumCollector
    """

    # setting constants
    QUERYLIMIT = 50
    FILESDIR = 'albumfiles'
    ALBUMLIMIT = 5

    def __init__(self, client=spotipy.Spotify()):
        """
        Initializes an empty collector

        Args:
            client : spotipy Spotify client with right credentials
        """
        super().__init__(client)
        self._request = GetRequest()
        self._artists = ArtistCollector()
        self._items = AlbumCollection()

    def get(self, limit=float('inf'), lowestpopularity=0):
        """
        Tries to get some albums with popularity that is
        higher than lowestpopularity

        Args:
             limit (int): maximal number of artists,
                 whose albums should be analyzed
             lowestpopularity (int): lowest popularity of the albums,
                 that will be added to a collector
        """
        assert(isinstance(limit, int) or isinstance(limit, float))
        assert(isinstance(lowestpopularity, int))
        try:
            self._get(limit, lowestpopularity)
        except:
            pass

    def __getitem__(self, item):
        """
        Returns:
            item attribute of AlbumCollector

        see Collector.__getitem__ for more details
        """
        try:
            return super().__getitem__(item)
        except:
            if item == 'artists':
                return self._artists
            else:
                raise KeyError

    def _get(self, limit, lowestpopularity):
        """
        Helper method to get albums
        """
        print("\nCollecting\n")
        overallcounter = 0
        counter = 0

        i = self['artists'].__iter__()
        while counter < self['request']['n'] + 1:
            counter += 1
            artist = i.__next__()

        while overallcounter < limit:
            albumsearch = self['client'].artist_albums(artist.id(),
                                                       limit=self.ALBUMLIMIT)

            albumsidlist = [item["id"] for item in albumsearch["items"]]
            albumsfull = self['client'].albums(albumsidlist)

            for albumfull in albumsfull["albums"]:
                album = Album.process_from_request(albumfull)
                if album.popularity() >= lowestpopularity:
                    self['items'].add(album)

            self['request']['n'] += 1
            overallcounter += 1
            artist = i.__next__()

            print('\r' + "COLLECTING DATA " + str(overallcounter), end='')

    def load(self, artistsfolder, albumfolder, printinfo=False):
        """
        loads currently available information about
        artists and albums

        Args:
            artistsfolder (str): name of the folder inside
                ArtistCollector.FILESDIR folder where data
                about artists is stored
            albumfolder (str): name of folder insode
                self.FILESDIR folder where data about
                albums is stored
            printinfo (bool): if True, show information about
                already loaded albums while working
        """
        try:
            artistsfile = open("%s/%s/items.txt" %
                               (ArtistCollector.FILESDIR, artistsfolder),
                               'r', encoding='utf8')
            self._artists = ArtistCollection.process_from_file(artistsfile,
                                                               printinfo)

            super().load(albumfolder, GetRequest, AlbumCollection, printinfo)
        except:
            pass


class SongCollector:
    """
    This class represents a song collector
    that stores data with no order and repetitions
    """

    # setting constants
    FILESDIR = 'songsfiles'

    def __init__(self, client=spotipy.Spotify()):
        """
        Initializes an empty collector

        Args:
            client : spotipy Spotify client with right credentials
        """
        self._client = client
        self._request = GetRequest()
        self._songs = SongCollection()
        self._features = FeatureCollection()
        self._albums = AlbumCollection()

    def __getitem__(self, item):
        """
        returns item attribute of SongsCollector instance

        Args:
            item (str): name of attribute of SongCollector
                that you need to access

        Returns:
             value of item attribute
             if there is no such an attribute,
             KeyError is raised
        """
        if item == 'client':
            return self._client
        if item == 'request':
            return self._request
        if item == 'songs':
            return self._songs
        if item == 'features':
            return self._features
        if item == 'albums':
            return self._albums
        raise KeyError

    def __iter__(self):
        """
        Returns:
             iterator for songs in the collector
        """
        return self['songs'].__iter__()

    def __contains__(self, item):
        """
        Args:
            item (str or Song instance): object that
                will be checked for presence
                in a collector

            you can check by instance or by its id
            (see Bag documentation)
        Returns:
             True if item is in a collector,
             False otherwise
        """
        return item in self['songs']

    def addsong(self, item):
        """
        Adds a song to a Collector

        Args:
            item (Song instance): song that will be added
                to a Collector
        """
        self['songs'].add(item)

    def addfeature(self, item):
        """
        Adds a feature to a Collector

        Args:
            item (Feature instance): feature that will be added
                to a Collector
        """
        self['features'].add(item)

    def get(self, limit=float('inf'), lowestpopularity=0):
        """
        Tries to get some albums' songs with popularity that is
            higher than lowestpopularity

        Args:
            limit (int): maximal number of albums,
                that should be analyzed
            lowestpopularity (int): lowest popularity of the songs,
                that will be added to a collector
        """
        assert (isinstance(limit, int) or isinstance(limit, float))
        assert (isinstance(lowestpopularity, int))
        try:
            self._get(limit, lowestpopularity)
        except:
            pass

    def _get(self, limit, lowestpoplarity):
        """
        Helper method to get songs
        """
        print("\nCollecting\n")

        overallcounter = 0
        counter = 0
        albumiterator = self['albums'].__iter__()

        while counter < self['request']['n'] + 1:
            counter += 1
            album = albumiterator.__next__()

        while overallcounter < limit:
            songidlist = [item for item in album.songs()]

            songsfull = self['client'].tracks(songidlist)
            featuresfull = self['client'].audio_features(songidlist)

            for i in range(len(songsfull['tracks'])):
                tempsong = Song.process(songsfull['tracks'][i])

                if (tempsong.popularity() >= lowestpoplarity and
                    featuresfull[i] is not None):
                    tempfeature = Feature.process(featuresfull[i])
                    if tempfeature.check():
                        self['features'].add(tempfeature)
                        self['songs'].add(tempsong)

            overallcounter += 1
            self['request']['n'] += 1
            album = albumiterator.__next__()

            print('\r' + "COLLECTING DATA " + str(overallcounter), end='')

    def save(self, foldername, printinfo=False):
        """
        Saves currently available information
        to folder named fordername which will be located
        inside self.FILESDIR directory

        args:
            foldername (str): name of the folder
                where data will be stored (see above for more detail)
            printinfo (bool): if True, show information about
                already saved songs while working
        """
        self.prepare_dir()
        counter = 0
        print("\nSaving Songs\n")

        path = self.FILESDIR + '/' + foldername
        if not os.path.isdir(path):
            os.mkdir(path)

        songsfile = open(path + '/songs.txt', 'w', encoding='utf8')
        featuresfile = open(path + '/features.txt', 'w', encoding='utf8')
        requestfile = open(path + '/request.py', 'w', encoding='utf8')

        for line in self['songs'].pythoncode():
            counter += 1
            if printinfo:
                print("\r" + "SAVING DO NOT QUIT " + str(counter), end='')
            songsfile.write(line + '\n')

        counter = 0
        if printinfo:
            print()
        print("\nSaving Features\n")

        for line in self['features'].pythoncode():
            counter += 1
            if printinfo:
                print("\r" + "SAVING DO NOT QUIT " + str(counter), end='')
            featuresfile.write(line + '\n')

        requestfile.write(repr(self['request']))

        songsfile.close()
        featuresfile.close()
        requestfile.close()

    def load(self, albumsfolder, songsfolder, printinfo=False):
        """
        loads information about albums,
        songs and features that are stored
        in AlbumCollector.FILESDIR/albumsfolder
        and self.FILESDIR/songsfolder respectively

        Args:
            albumsfolder (str): name of the folder where
                info about albums is stored
            songsfolder (str): name of the folder where
                info about songs and features is stored
            printinfo (bool): if True, show information about
                already loaded songs while working
        """
        try:
            albumsfile = open("%s/%s/items.txt" %
                              (AlbumCollector.FILESDIR, albumsfolder),
                              'r', encoding='utf8')
            self._albums = AlbumCollection.process_from_file(albumsfile,
                                                             printinfo)

            requestmodule = importlib.import_module("%s.%s.request" %
                                                    (self.FILESDIR,
                                                     songsfolder))
            self._request = GetRequest.process_from_file(requestmodule.request)

            songsfile = open("%s/%s/songs.txt" %
                             (self.FILESDIR, songsfolder),
                             'r', encoding='utf8')
            self._songs = SongCollection.process_from_file(songsfile,
                                                           printinfo)

            featuresfile = open("%s/%s/features.txt" %
                                (self.FILESDIR, songsfolder),
                                'r', encoding='utf8')
            self._features = FeatureCollection.process_from_file(featuresfile,
                                                                 printinfo)
        except:
            pass

    @classmethod
    def prepare_dir(cls):
        """
        Checks if folder with collector files exists
        If not, creates this folder
        """
        if not os.path.isdir(cls.FILESDIR):
            os.mkdir(cls.FILESDIR)
