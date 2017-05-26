# soundcloud python sdk usage example
# search for 2 the most popular song of an artist in the US
# prints basic information about this artist
# also analysis of this song is printed
# name of the artist is entered by a user
# see spotify.txt for an example(in that case the query is 'bieber')

# importing modules
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import string

# setting client credentials
client_credentials_manager = SpotifyClientCredentials("YOUR_CLIENT_ID","YOUR_CLIENT_SECRET")
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace=False

# getting request from user
request = input()
request.strip()

# deleting punctuation and replacing spaces with "%20"
delete_punctuation = lambda x: x if x == ' ' or x in string.ascii_letters else ''
replace_space = lambda x: x if x != ' ' else "%20"
request = ''.join([delete_punctuation(x) for x in request])
request = ''.join([replace_space(x) for x in request])

# searching for an artist
artists = sp.search(q=request, limit=1, type='artist')
for artist in artists['artists']['items']:

    # displaying information about an artist
    print("ARTIST INFORMATION")
    print("Artist name:", artist['name'])
    print("Artist id:", artist['id'])
    print("Artist popularity:", artist['popularity'])

    # getting top tracks of an artist
    tracks = sp.artist_top_tracks(artist['id'])
    print('_______________________')
    print()
    print('_______________________')
    for track in tracks['tracks'][:2]:
        print("\tTrack title:",track['name'])
        print("\tTrack id:",track['id'])

        # getting features of a particular track
        features = sp.audio_features(track['id'])[0]
        print("\t\tTrack loudness", features['loudness'])
        print("\t\tTrack liveness", features['liveness'])
        print("\t\tTrack acousticness", features['acousticness'])
        print("\t\tTrack speechiness", features['speechiness'])
