import json

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


songs = TimeRange(1956, 2017, s, f, a, 0)
songs.addall(True)

result = {}
for item in songs:
    result[item['name']] = [len(item._songs), item._albums.get_length()]
with open('webinfo/years_number_data.txt', 'w', encoding='utf8') as file1:
    file1.write(json.dumps(result))

songs = TimeRange(2000, 2017, s, f, a, 18)
songs.addall(True)
result = {}
for item in songs:
    result[item['name']] = [len(item._songs), item._albums.get_length()]
with open('webinfo/quarters_number_data.txt', 'w', encoding='utf8') as file2:
    file2.write(json.dumps(result))

