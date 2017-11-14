<h1>Music Explorer</h1>


Web platform that helps you to find the closest songs to your playlist as well as the alternative ones.
<br /><br />

It consists of 2 parts:<br />
* scripts for <b>scrabbing data</b> using spotify api, form <b>reports</b> and <b>statistics</b>
* scripts for web interface that will help you to find <b>closest and alternative songs</b> to your playlist and form <b>interactive reports</b> on analyzed songs

<br /><br />

You can check <b>scrubbing architecture</b> [here](doc/classdiagram.html)<br />
What it cans:
* scrub general information about the <b>most popular artists on Spotify</b> [usage example](collect_artists.py)
* scrub general information about the <b>albums</b> of the collected artists [usage example](collect_albums.py)
* scrub the <b>general and particular information</b> about the <b>songs</b> in collected albums [usage example](collect_songs.py)
* save/load all the data mentioned above
* form <b>report</b> on the scrubbed data [possible result](result.txt)

<br /><br />

What does the <b>platform</b> can:
* form <b>reports</b>(graphs) on <b>particular feature</b> of the songs(acousticness, loudness, etc) on <b>particular timerange</b> [example](examples/web_platform_examples/graph.jpg)
* form a <b>playlist</b> by searching for songs on spotify [example](examples/web_platform_examples/playlist_creation.jpg)
* create playlist of <b>similar</b> and <b>alternative</b> songs by comparing middle characteristics of the songs in the playlist with scrubbed songs [example](examples/web_platform_examples/suggestions.jpg)<br/> 
(<b>WARNING</b>: as it is written in pure python, the response time is very big (~30 sec/request). I am currently thinking about rewriting it in low-level language(C++ for example) to make it run faster and apply normalization techniques to produce better results)

