import json


from musicitem import *
from collection import *
from bag import *
from arrays import *


class TimeRange:
    """
    This class represents a larger period
    of time that consists of some subperiods(TimeDelta instances)
    """

    # setting constants
    # endings of quarters ordinals
    ENDINGS = ["st", "nd", "rd", "th"]

    @classmethod
    def readfromfile(cls,
                     text,
                     startyear,
                     endyear,
                     songcollection,
                     featurecollection,
                     albumcollection,
                     QUARTERYEARSNUM=15):
        temp = TimeRange(startyear,
                         endyear,
                         songcollection,
                         featurecollection,
                         albumcollection,
                         QUARTERYEARSNUM)
        i = -1
        iterator = text.__iter__()
        for i in range(len(temp._pieces) - temp.QUARTERYEARSNUM):
            line = iterator.__next__()
            temp._pieces[i] = TimeDelta.readfromfile(featurecollection, line)
        for special in range(i + 1, len(temp._pieces)):
            temp._pieces[special] = Array(4)
            for quarternum in range(1, 5):
                line = iterator.__next__()
                temp._pieces[special][quarternum - 1] = TimeDelta.readfromfile(
                    featurecollection, line
                )
        return temp

    def __init__(self,
                 startyear,
                 endyear,
                 songcollection,
                 featurecollection,
                 albumcollection,
                 QUARTERYEARSNUM=15):
        """
        initializes new TimeRange instance as an array
        of TimeDelta instances

        last QUARTERYEARSNUM years will be divided into quarters

        Args:
            startyear (int): number of the smallest year
                in timerange. All songs, that were released earlier,
                will be ignored
            endyear (int): number of the last year in timerange.
                All songs, that were released after this year,
                will be ignored
            songcollection (SongCollection): collection of the songs
                that will be analyzed
            featurecollection (FeatureCollection): collection of features
                of the songs that will be analyzed
            albumcollection (AlbumCollection): collection of the albums
                of the songs that will be analyzed
            QUARTERYEARSNUM(int): number of last years that will be
                divided into quarters

        if year has wrong type or format, AssertionError is raised
        """
        assert(isinstance(startyear, int))
        assert(isinstance(endyear, int))
        assert(startyear <= endyear)
        self._songs = songcollection
        self._albums = albumcollection
        self._features = featurecollection
        self._pieces = Array(endyear - startyear + 1)
        self._startyear = startyear
        self._endyear = endyear
        self.QUARTERYEARSNUM = QUARTERYEARSNUM
        i = -1
        for i in range(len(self._pieces) - self.QUARTERYEARSNUM):
            self._pieces[i] = TimeDelta(str(startyear + i), self._features)
        for special in range(i + 1, len(self._pieces)):
            self._pieces[special] = Array(4)
            for quarternum in range(1, 5):
                name = (str(startyear + special) + ' ' +
                        str(quarternum) +
                        self.ENDINGS[quarternum - 1] +
                        " quarter")
                self._pieces[special][quarternum - 1] = TimeDelta(
                    name, self._features)



    def __iter__(self):
        """
        Returns:
            generator for all time deltas in TimeRange instance
        """
        i = -1
        for i in range(len(self._pieces) - self.QUARTERYEARSNUM):
            yield self._pieces[i]
        for special in range(i + 1, len(self._pieces)):
            for quarternum in range(4):
                yield self._pieces[special][quarternum]

    def getreport(self, songsnum=0):
        """
        Args:
             songsnum (int): number of the most popular
                songs that will be included in each of the reports
                on particular TimeDelta

        Returns:
            generator for reports about all available
            timedeltas in self
        """
        print('forming general report...')
        assert (isinstance(songsnum, int))
        assert (songsnum >= 0)
        songsnum = min(songsnum, TimeDelta.MAXSONGREPORTNUM)
        for piece in self:
            yield piece.getreport(songsnum)

    def isquarter(self, yearnum):
        """
        Args:
            yearnum (int): number of the year that is in
                [startyear; endyear]

        Returns:
            True if yearnum should be divided into quarters,
            False otherwise
        """
        return not yearnum < self._endyear - self.QUARTERYEARSNUM + 1

    def getyearindex(self, yearnum):
        """
        Args:
             yearnum (int): number of the year that is in
                [startyear; endyear]
        Returns:
            index of the yearnum year in the array
            of timedeltas
        """
        return yearnum - self._startyear

    def getquarterindex(self, month):
        """
        Args:
             month (int): number of months in [1;12]

        Returns:
            index of the quarter of a particular month (in [0; 3])
        """
        return (month - 1) // 3

    def _add(self, song):
        """
        Helper method for adding Song instance to a relevant
        timedelta
        """
        songreleasedate = self._albums[song.albumid()].release_date()
        year = songreleasedate[0]
        if year >= self._startyear and year <= self._endyear:
            if not self.isquarter(year):
                self._pieces[self.getyearindex(year)].add(song)
            else:
                if len(songreleasedate) == 2:
                    month = songreleasedate[1]
                    self._pieces[self.getyearindex(year)][self.getquarterindex(month)].add(song)

    def addall(self, printinfo=False):
        """
        Adds all currently available songs to a TimeRange instance,
        dividing them in relevant TimeDeltas

        if there is no quarter precision for the song when it is needed,
        this song is ignored
        Args:
             printinfo (bool): if True,
                prints information about alredy
                added songs while working
        """
        print("adding songs...")
        counter = 0
        for item in sorted(self._songs,
                           key=lambda x: x.popularity(),
                           reverse=True):
            if printinfo:
                counter += 1
                if counter % 1000 == 0:
                    print('\rAdding ' + str(counter), end='')
            self._add(item)


class TimeDelta:
    """
    This class represents information about particular
    period of time and contains information about the songs,
    average characteristics and most popular songs during this period
    """

    # setting constants

    # max number of popular songs that will be displayed
    MAXSONGREPORTNUM = 5
    # characteristics of the song that has no discrete options
    NONDISCRETEARGS = ['acousticness',
                       'danceability',
                       'energy',
                       'instrumentalness',
                       'speechiness',
                       'valence',
                       'duration_ms',
                       'loudness',
                       'tempo']
    # characteristics of the song that varies from 0.0 to 1.0
    NONPERCENTAGEDARGS = NONDISCRETEARGS[-3:]

    PERCENTAGEDARGS = NONDISCRETEARGS[:-3]
    # names of discrete arguments and their options
    DISCRETEARGS = {'mode': [0, 1],
                    'key': list(range(12)),
                    'time_signature': list(range(11))}
    # accessible attributes of TimeDelta class
    ATTRS = ['name',
             'all_popularity',
             'middle_feature',
             'feature_collection',
             'albums',
             'extreme_nums',
             'discrete',
             'songs']

    def __init__(self,
                 name,
                 feature_collection,
                 arraysize=1000):
        """
        initializes new TimeDelta instance
        sets default min and max values of some characteristics of the songs

        Args:
            name (str): name of the period of time
            feature_collection (FeatureCollection): collection of the
                features of the songs that will be added
            arraysize (int): start size of array with songs
        """
        self._name = name
        self._all_popularity = 0
        self._middle_feature = Feature()
        self._feature_collection = feature_collection
        self._albums = SimpleBag()
        self._extreme_nums = {'max': {}, 'min': {}}
        for item in self.NONDISCRETEARGS:
            self._extreme_nums['max'][item] = {}
            self._extreme_nums['min'][item] = {}
            self._extreme_nums['max'][item]['value'] = (-1) * float('inf')
            self._extreme_nums['max'][item]['id'] = None
            self._extreme_nums['min'][item]['value'] = float('inf')
            self._extreme_nums['min'][item]['id'] = None
        self._discrete = {}
        for item in self.DISCRETEARGS:
            self._discrete[item] = {}
            for option in self.DISCRETEARGS[item]:
                self._discrete[item][option] = 0
        self._songs = DynamicArray(arraysize)

    @classmethod
    def readfromfile(cls, feature_collection, text):
        info = json.loads(text)
        if len(info['songs']) == 0:
            return None
        temp = TimeDelta(info['name'], feature_collection, len(info['songs']))
        temp._middle_feature = Feature.process_from_file(eval(info['middle_feature']))
        temp._extreme_nums = info['extreme_values']
        temp._discrete = info['discrete_values']
        for i in range(len(info['songs'])):
            tempsong = Song.process_from_file(eval(info['songs'][i]))
            temp._songs.append(tempsong)
            temp._all_popularity += tempsong.popularity()
        return temp

    def savetofile(self, songsnum):
        """
        Args:
            songsnum(int): first songsnum songs will be added
                to representation of the instance

        Returns:
             str: json encoded information about
             TimeDelta instance that will consist of:
                1) name
                2) middle_feature
                3) extreme values
                4) discrete values
                5) id of first songs
        """
        songsnum = min(songsnum, len(self._songs))
        result = {}
        result['name'] = self._name
        result['middle_feature'] = repr(self._middle_feature)
        result['extreme_values'] = self._extreme_nums
        result['discrete_values'] = self._discrete
        tempsongs = []
        for i in range(songsnum):
            tempsongs.append(repr(self._songs[i]))
        result['songs'] = tempsongs
        return json.dumps(result)


    def __getitem__(self, item):
        """
        Tries to return item attribute of an instance
        Raises KeyError if there is no such an attribute

        Args:
             item (str): name og the attribute that needed to be accessed
                see self.ATTRS for list of available attributes
        """
        if item not in self.ATTRS:
            raise KeyError
        return eval('self._%s' % (item))

    def add(self, song):
        """
        Args:
            song (Song): song instance that needed to be added

        Adds song to timedelta instance
        updates min and max values
        """
        self._all_popularity += song.popularity()
        self._albums.add(song.albumid())

        for item in self.DISCRETEARGS:
            self._discrete[item][self._feature_collection[song.id()][item]] += \
                song.popularity()

        for item in self.NONDISCRETEARGS:
            tempvalue = self._feature_collection[song.id()][item]
            if self._extreme_nums['min'][item]['value'] > tempvalue:
                self._extreme_nums['min'][item]['value'] = tempvalue
                self._extreme_nums['min'][item]['id'] = song.id()
            if self._extreme_nums['max'][item]['value'] < tempvalue:
                self._extreme_nums['max'][item]['value'] = tempvalue
                self._extreme_nums['max'][item]['id'] = song.id()

        self['songs'].binary_insert(song)

    def create_middle_feature(self,
                              n=float('inf')):
        """
        Calculates middle characteristics of n most popular
            songs in this period according to its popularity

        Args:
             n (int): number of songs that should be counted
             allpopularity (int): total popularity of the first n songs
        """
        if n == float('inf'):
            allpopularity = self._all_popularity
            custom = False
        else:
            custom = True
            allpopularity = 0
            for i in range(min(n, len(self['songs']))):
                allpopularity += self['songs'][i].popularity()
        print('finding middle values for %s...' % self._name)
        temp = Feature()
        counter = 0
        for item in self['songs']:
            counter += 1
            for f in self.NONDISCRETEARGS:
                temp[f] += \
                    ((item.popularity() * self._feature_collection[item.id()][f])/
                     allpopularity)
            if counter >= n:
                break
        if custom:
            return temp
        else:
            self._middle_feature = temp


    def getk(self, feature):
        """
        Returns overall coefficient that shows how much
        a particular song differs from
        middle song of a period

        Coefficient is calculated as sum of absolute difference
        (in percents from 0 to 1) of all non discrete parameters

        Args:
            feature (Feature): song that will be compared
        Returns:
            overall coefficient of difference
        """
        result = 0
        for item in self.PERCENTAGEDARGS:
            if item == 'speechiness':
                continue
            result += abs(feature[item] - self._middle_feature[item])
        for item in self.NONPERCENTAGEDARGS:
            if item == 'duration_ms':
                continue
            f = abs(self._middle_feature[item])
            c = abs(feature[item])
            result += abs(1 - min(f, c)/max(f,c))
        return result

    def find_closest(self):
        """
        Search through all the songs of the peroid
        and finds the songs with the smallest coefficient of difference

        Returns:
            list of the songs that has the smallest
            coefficient of difference (see self.getk() documentation)
        """
        print('finding closest for %s...' % self._name)
        resultidlist = []
        resultk = float('inf')
        for item in self['songs']:
            currentresult = self.getk(self._feature_collection[item.id()])
            if currentresult == resultk:
                resultidlist.append(item.id())
            if currentresult < resultk:
                resultidlist = [item.id()]
                resultk = currentresult
        return resultidlist

    def getreport(self, songsnum=0):
        """
        Froms the report about this period
            of time and return it as list of strings
            that should be printed in separate lines

        Report format:
        - name of the period of time
        - totally analyzed songs
        - totally analyzed albums
        - most popular songs
        - average characteristics of the first 5 songs
        - average characteristics of all the songs
        - the closest song for average parameters
        - songs with maximal characteristics
        - songs with minimal characteristics
        - percentage of all discrete characteristics of the song

        Args:
             songsnum (int): number of the most popular
                songs that will be included in the report
        Returns:
            textual representation of the report

        if songsnum has wrong format or value, AssertionError is raised
        """
        assert(isinstance(songsnum, int))
        assert(songsnum >= 0)
        print('forming report for %s...' % self._name)
        songsnum = min(songsnum, self.MAXSONGREPORTNUM)
        result = []
        result.append("Timedelta %s" % (self._name))
        result.append("Totally analyzed %s song(s)" % len(self._songs))
        if len(self._songs) == 0:
            result.append('---------------------')
            return result
        result.append("Totally analyzed %s album(s)" %
                      (self._albums.get_length()))
        result.append("Most popular songs(spotify id and popularity):")
        for i in range(min(songsnum, len(self._songs))):
            result.append("\t%s - %s" % (self._songs[i].popularity(),
                                  self._songs[i].id()))
        result.append("Average parameters of the most popular songs")
        n = 5
        popularity = 0
        counter = 0
        for item in self._songs:
            counter += 1
            popularity += item.popularity()
            if counter >= n:
                break
        self.create_middle_feature(n, popularity)
        for item in self.NONDISCRETEARGS:
            result.append("\t %s : %s" % (item, self._middle_feature[item]))
        self.create_middle_feature()
        result.append("Average parameters of the songs:")
        for item in self.NONDISCRETEARGS:
            result.append("\t %s : %s" % (item, self._middle_feature[item]))
        result.append("Closest songs(spotify ids):")
        counter = 0
        for item in self.find_closest():
            counter += 1
            result.append("\t%s) %s" %(str(counter), item))
            for option in self.NONDISCRETEARGS:
                result.append("\t\t%s : %s" %
                              (option,
                               self._feature_collection[item][option]))
        result.append("Extremal values:")
        result.append("\tMax (name: value (song id))")
        for item in self._extreme_nums['max']:
            result.append("\t\t%s : %s (%s)" %
                          (item,
                           str(self._extreme_nums['max'][item]['value']),
                           self._extreme_nums['max'][item]['id']))
        result.append("\tMin (name: value (song id))")
        for item in self._extreme_nums['min']:
            result.append("\t\t%s : %s (%s)" %
                          (item,
                           str(self._extreme_nums['min'][item]['value']),
                           self._extreme_nums['min'][item]['id']))
        result.append("Percentage:")
        for item in self.DISCRETEARGS:
            result.append("\t%s" % item)
            for option in self._discrete[item]:
                val = self._discrete[item][option]
                if val > 0:
                    result.append("\t\t%s : %s%%" %
                                  (str(option),
                                   str(val*100/self._all_popularity)))
        result.append('---------------------')
        return result
