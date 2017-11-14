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

def add():
    for item in t:
        if item is None:
            continue
        for song in item._songs:
            news.add(song)
            newf.add(f[song.id()])
        for name in item._extreme_nums['min']:
            id = item._extreme_nums['min'][name]['id']
            if id is not None:
                news.add(s[id])
                newf.add(f[id])
        for name in item._extreme_nums['max']:
            id = item._extreme_nums['max'][name]['id']
            if id is not None:
                news.add(s[id])
                newf.add(f[id])

text = open('webinfo/years.txt')
t = TimeRange.readfromfile(text, 1956, 2017, s, f, a, 0)
news = SongCollection()
newf = FeatureCollection()
add()
with open('webinfo/songs_years.txt', 'w', encoding='utf8') as sfile:
    for item in news:
        sfile.write(repr(item) + '\n')
with open('webinfo/features_years.txt', 'w', encoding='utf8') as ffile:
    for item in newf:
        ffile.write(repr(item) + '\n')
text.close()

text = open('webinfo/quarters.txt')
t = TimeRange.readfromfile(text, 2000, 2017, s, f, a, 18)
news = SongCollection()
newf = FeatureCollection()
add()
with open('webinfo/songs_quarters.txt', 'w', encoding='utf8') as sfile:
    for item in news:
        sfile.write(repr(item) + '\n')
with open('webinfo/features_quarters.txt', 'w', encoding='utf8') as ffile:
    for item in newf:
        ffile.write(repr(item) + '\n')
text.close()
text.close()
