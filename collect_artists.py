# this module is used to collect information
# about the most famous artists according to their popularity
# use your Spotify Credentials in case it to work properly

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from collector import *


client_credentials_manager = SpotifyClientCredentials("e0a05f437d6c479f9baf1d35f459da8a",
                                                      "ec8922d4733c412e8dc0b0ddfb075bc9")
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace=False


c = ArtistCollector(sp)
c.load('test')

c.get(limit=50, lowestpopularity=20)

c.save('test')
