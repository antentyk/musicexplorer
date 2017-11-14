# Music Explorer


Web platform that helps you to find the closest songs to
your playlist as well as the alternative ones.


It consists of 2 parts:
	- scripts for scrapping data using spotify api, form reports and statistics
	- scripts for displaying web interface and search for closest and alternative songs


You can check scrabbing architecture in doc/classdiagram.html
What it cans:
	- scrab general information about the most popular artists on Spotify(check collect_artists.py)
	- scrab general information about the albums of the collected artists(check collect_albums.py)
	- scrab the general and particular information about the songs in collected albums(check collect_songs.py)
	- save/load all the data mentioned above
	- form report on the scrabbed data (check result.txt and result1.txt)

What does the platform can:
	- form reports(graphs) on particular feature of the songs(acousticness, loudness, etc) on particular timerange
	- form a playlist by searching for songs on spotify
	- create playlist of similar and alternative songs by comparing middle characteristics of the songs in the playlist with scrabbed songs (WARNING: as it is written in pure python, the response time is very big (~30 sec/request). I am currently thinking about rewriting it in low-level language(C++ for example) to make it run faster and apply normalization techniques to produce better results)

