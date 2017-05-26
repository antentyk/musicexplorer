# this module is used to collect information
# about the songs of the albums that were already collected
# in collect_albums.py
# do not collect any extra albums in the folder that you are using
# because song collection won't work properly
# use valid Spotify credentials to make it work

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from collector import *

client_credentials_manager = SpotifyClientCredentials("e0a05f437d6c479f9baf1d35f459da8a",
                                                      "ec8922d4733c412e8dc0b0ddfb075bc9")
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace=False

s = SongCollector(sp)

s.load('test', 'test')

s.get(limit=30, lowestpopularity=20)

s.save('test')
