import json


from collection import *
from bag import *
from musicitem import *
from arrays import *
from analysis import *


songsyearsfile = open('webinfo/songs_years.txt', encoding='utf8')
featuresyearsfile = open('webinfo/features_years.txt', encoding='utf8')

songs_years = SongCollection.process_from_file(songsyearsfile)
features_years = FeatureCollection.process_from_file(featuresyearsfile)

songsyearsfile.close()
featuresyearsfile.close()

songsquartersfile = open('webinfo/songs_quarters.txt', encoding='utf8')
featuresquartersfile = open('webinfo/features_quarters.txt', encoding='utf8')

songs_quarters = SongCollection.process_from_file(songsquartersfile)
features_quarters = FeatureCollection.process_from_file(featuresquartersfile)

songsquartersfile.close()
featuresquartersfile.close()


numberfile = open('webinfo/years_number_data.txt')
years_numbers = json.loads(numberfile.read().strip())
numberfile.close()


numberfile = open('webinfo/quarters_number_data.txt')
quarters_numbers = json.loads(numberfile.read().strip())
numberfile.close()

songs = SongCollection()
features = FeatureCollection()
for item in songs_quarters:
    songs.add(item)
for item in songs_years:
    songs.add(item)
for item in features_quarters:
    features.add(item)
for item in features_years:
    features.add(item)

year_range_file = open('webinfo/years.txt', encoding='utf8')
year_range = TimeRange.readfromfile(year_range_file,
                                    1956,
                                    2017,
                                    songs_years,
                                    features_years,
                                    None,
                                    0)
year_range_file.close()


quarter_range_file = open('webinfo/quarters.txt', encoding='utf8')
quarter_range = TimeRange.readfromfile(quarter_range_file,
                                       2000,
                                       2017,
                                       songs_quarters,
                                       features_quarters,
                                       None,
                                       18)
quarter_range_file.close()