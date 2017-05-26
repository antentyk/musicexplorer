# this module is used to divide currently
# available songs by years and quarters
# and get report about all the time delta that was set


from collection import *
from bag import *
from musicitem import *
from arrays import *
from analysis import *


songsfile = open('songsfiles/test/songs.txt', encoding='utf8')
featuresfile = open('songsfiles/test/features.txt', encoding='utf8')
albumsfile = open('albumfiles/test/items.txt', encoding='utf8')

s = SongCollection.process_from_file(songsfile)
f = FeatureCollection.process_from_file(featuresfile)
a = AlbumCollection.process_from_file(albumsfile)

songsfile.close()
featuresfile.close()
albumsfile.close()

s = TimeRange(2012, 2017, s, f, a)
s.addall(True)

resfile = open('result.txt', 'w', encoding='utf8')
for smallreport in s.getreport(15):
    for line in smallreport:
        resfile.write(line + '\n')
resfile.close()