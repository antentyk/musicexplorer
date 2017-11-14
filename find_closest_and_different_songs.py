import json


from auth import sp as client

from analysis import TimeDelta
from musicitem import Feature, Song
from collection import FeatureCollection, SongCollection


def find(songsinfo, features):
    idlist = [item[0] for item in songsinfo]

    playlistsongs = SongCollection()
    playlistfeatures = FeatureCollection()
    playlistfeaturesraw = client.audio_features(idlist)

    for i in range(len(songsinfo)):
        try:
            tempfeature = Feature.process(playlistfeaturesraw[i])
            if tempfeature.check():
                tempsong = Song(songsinfo[i][0], None, songsinfo[i][1])
                playlistsongs.add(tempsong)
                playlistfeatures.add(tempfeature)
        except:
            pass

    playlist = TimeDelta('playlist', playlistfeatures, 10)
    for item in playlistsongs:
        playlist.add(item)
    playlist.create_middle_feature()

    similar = [(float('inf'), '') for i in range(5)]
    different = [((-1) * float('inf'), '') for i in range(5)]

    for feature in features:
        if feature['id'] in playlistsongs:
            continue
        samesong = False
        for item in playlistsongs:
            if playlistfeatures[item.id()].equal_characteristics(feature):
                samesong = True
                break
        if samesong: continue
        for item in similar + different:
            if item[1] != "" and feature.equal_characteristics(features[item[1]]):
                samesong = True
                break
        if samesong: continue
        k = playlist.getk(feature)
        t = (k, feature['id'])
        if t < similar[4]:
            counter = 0
            while counter < 5:
                if t < similar[counter]:
                    break
                counter += 1
            for i in range(4, counter, -1):
                similar[i] = similar[i - 1]
            similar[counter] = t
        if t > different[4]:
            counter = 0
            while counter < 5:
                if t > different[counter]:
                    break
                counter += 1
            for i in range(4, counter, -1):
                different[i] = different[i - 1]
            different[counter] = t

    similaridlist = [item[1] for item in similar]
    differentidlist = [item[1] for item in different]

    result = {}

    response = client.tracks(similaridlist)
    result['similar'] = [(item['id'],
                item['uri'],
                item['name'],
                item['artists'][0]['name'],
                item['popularity'])
                for item in response['tracks']]

    response = client.tracks(differentidlist)
    result['different'] = [(item['id'],
                item['uri'],
                item['name'],
                item['artists'][0]['name'],
                item['popularity'])
                for item in response['tracks']]

    return json.dumps(result)