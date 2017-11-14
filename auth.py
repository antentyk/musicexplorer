import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


cred = SpotifyClientCredentials("e0a05f437d6c479f9baf1d35f459da8a",
                                "917659bc4de34d1891f1f16aef574a1d")
sp = spotipy.Spotify(client_credentials_manager=cred)
sp.trace=False
