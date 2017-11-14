from collection import *
from bag import *
from musicitem import *
from arrays import *
from analysis import *


songsfile = open('songsfiles/trial/songs.txt', encoding='utf8')
featuresfile = open('songsfiles/trial/features.txt', encoding='utf8')
albumsfile = open('albumfiles/trial/items.txt', encoding='utf8')

s = SongCollection.process_from_file(songsfile)
f = FeatureCollection.process_from_file(featuresfile)
a = AlbumCollection.process_from_file(albumsfile)

songsfile.close()
featuresfile.close()
albumsfile.close()

songs = TimeRange(2000, 2017, s, f, a, 18)
songs.addall(True)

with open('webinfo/quarters.txt', 'w', encoding='utf8') as file1:
    for item in songs:
        item.create_middle_feature()
        item._songs._resize(500)
        file1.write(item.savetofile(500) + '\n')

songs = TimeRange(1956, 2017, s, f, a, 0)
songs.addall(True)

with open('webinfo/years.txt', 'w', encoding='utf8') as file2:
    for item in songs:
        item.create_middle_feature()
        item._songs._resize(500)
        file2.write(item.savetofile(500) + '\n')