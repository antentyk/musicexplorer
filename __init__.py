from flask import Flask, render_template, request
import json


import search_songs
from get_collections import *
from analysis import TimeDelta
from musicitem import Song
import find_closest_and_different_songs
import handle_graphs_building


app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/suggest')
def suggest():
    return render_template('suggest.html')


@app.route('/search_tracks', methods=['GET','POST'])
def tracks():
    query = request.form['query']
    return json.dumps(search_songs.search(query))


@app.route('/find_closest', methods=['POST'])
def find_closest():
    songsinfo = [[item[0], item[4]] for item in
              filter(lambda x: len(x) > 0, request.json['playlist'])]
    return find_closest_and_different_songs.find(songsinfo, features)

@app.route('/analyze')
def analyze():
    return render_template('analyze.html')

@app.route('/get_graphs_data', methods=['POST'])
def get_graphs_data():
    return json.dumps(handle_graphs_building.build_graphs(request.form, year_range, quarter_range))

app.run(debug=True)
