'''
Name: idk (Borealis?)

Description:
- No authentication required for v0.5
    - Could add auth for v1 to add to library
- simple UI, only audio visualization, current song, upcoming song
- opening page is search bar with app name above it
- Background is sound waves of current song play
    - before song input it will be default waves
    - if song is paused waves stop
- after first song input, embed spotify player over waves
    - spotify player oEmbed API
    - waves will implement first data structure
- allow like or dislike to influence radio algorithm
'''

import os
import random

import flask
import requests
import uuid
import urllib
import webbrowser
import json
import sys
from flask_cors import CORS

# Spotipy library might be easier than direct requests with api
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

'''
Setup
'''

HOST_IP_ADDRESS = 'localhost'
HOST_PORT = '8080'

# Env vars
# USERNAME = os.environ['SpotifyUser']
CLIENT_ID = os.environ.get('BorealisCID')
CLIENT_SECRET = os.environ.get('BorealisSecret')

SCOPE = ''
REDIRECT_URI = 'http://localhost:8080/start'

app = flask.Flask('Borealis')
CORS(app)
# Test env vars can be read (for mac in ~/.zshenv)
# print(CLIENT_ID)
# print(CLIENT_SECRET)

SP = spotipy.Spotify()

# keep track of played song ids
PLAYED = set()
SEED_TRACKS = PLAYED

# get recommendation tracks to make up radio queue
queue = []

# generate radio queue by getting similar song
# current_track = queue.pop()
# play current song
# if disliked then remove from seed_tracks and skip to next track

# request to api for audio analysis of song - WORKS
# audio_analysis = sp.audio_analysis(song_id)


@app.route('/play', methods=['POST'])
def play():
    # grab user front-end 
    song_name = flask.request.json['song']
    artist = flask.request.json['artist']
    
    # authenticate with api
    sp = auth()
    song_id = generate(sp, song_name, artist)
    # visualize = sp.audio_analysis(song_id) #FIX

    # return oEmbed API response for spotify player and visuals
    return flask.jsonify(songEmbed(song_id))

def auth():
    token = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=SCOPE)
    return spotipy.Spotify(auth_manager=token)
 

def songEmbed(song_id):
    PLAYED.add(song_id)
    #
    pass

def generate(sp, song_name, artist):
    SP = sp
    current_track = sp.search(q='track:'+song_name+' artist:'+artist, type='track', limit=1)['tracks']['items'][0]
    song_id = current_track['id']
    PLAYED.add(song_id)
    artist_ids = set()
    genres = set()

    for artist in current_track['artists']:
        artist_ids.add(artist['id'])
        if 'genres' in artist:
            genres.update(artist['genres'])

    queue = sp.recommendations(seed_artists=artist_ids, seed_genres=genres, seed_tracks=SEED_TRACKS, country='US')['tracks']

    return song_id
    
def getRecs():
    gueue = SP.recommendations(seed_tracks=SEED_TRACKS, country='US')['tracks']

@app.route('/upNext', methods=['GET'])
def upNext():
    return flask.jsonify(next=queue[-1])

# set next song
@app.route('/next', methods=['GET'])
def next():
    song_id = queue.pop()
    SEED_TRACKS.add(song_id)
    html = songEmbed(song_id)
    # visualizer = SP.audio_analysis(song_id) #FIX

    return flask.jsonify(html)

@app.route('/action', methods=['POST'])
def action():
    act = flask.request.args['action']
    song_id = flask.request.args['song_id']
    if act == 'dislike':
        # re-generate queue
        SEED_TRACKS.discard(song_id)
        getRecs()
        return next()
    else:
        # add to user spotify library
        pass

if __name__ == '__main__':
    app.run(host=HOST_IP_ADDRESS, port=HOST_PORT, use_reloader=True, debug=True)