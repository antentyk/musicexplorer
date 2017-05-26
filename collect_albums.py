# this module is used to get information
# about most popular albums of the artists
# that were alredy collected
# it is assumed that you have already collected
# artists in collect_artsits.py
# do not collect any extra artists in the folder that you are using
# because albums collection won't work properly
# use valid Spotify credentials to make it work

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from collector import *


client_credentials_manager = SpotifyClientCredentials("e0a05f437d6c479f9baf1d35f459da8a",
                                                      "ec8922d4733c412e8dc0b0ddfb075bc9")
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace=False

c = AlbumCollector(sp)
c.load('test', 'test')

c.get(limit=20, lowestpopularity=20)

c.save('test')
