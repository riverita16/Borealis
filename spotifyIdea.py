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
from random import randint, shuffle

# Spotipy library might be easier than direct requests with api
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

HOST_IP_ADDRESS = '127.0.0.1'
HOST_PORT = '8080'

# Env vars
# USERNAME = os.environ['SpotifyUser']
CLIENT_ID = os.environ.get('BorealisCID')
CLIENT_SECRET = os.environ.get('BorealisSecret')

SCOPE = ''
REDIRECT_URI = 'http://127.0.0.1:8080/see'

welcome_text = '''''
We need a name ~ Borealis                                                                                                                                                                
'''''

# Test env vars can be read (for mac in ~/.zshenv)
# print(CLIENT_ID)
# print(CLIENT_SECRET)

# not necessary for v0.5
# token = util.prompt_for_user_token(USERNAME, SCOPE, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

token = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=SCOPE)
sp = spotipy.Spotify(auth_manager=token)

# grab song name from terminal (will become input forms in front-end)
# song_name = input('Song name: ').strip()
song_name = 'always something'

# grab artist from terminal
# artist = input('Artist: ').strip()
artist = 'cage the elephant'

# query api for song information 
# add input validation
current_track = sp.search(q='track:'+song_name+' artist:'+artist, type='track', limit=1)['tracks']['items'][0]
song_id = current_track['id']
artist_ids = set()
genres = set()

for artist in current_track['artists']:
    artist_ids.add(artist['id'])
    if 'genres' in artist:
        genres.update(artist['genres'])


# keep track of played song ids
played = set()
played.add(song_id)
seed_tracks = played

# get recommendation tracks to make up queue
queue = sp.recommendations(seed_artists=artist_ids, seed_genres=genres, seed_tracks=seed_tracks, country='US')['tracks']

# generate radio queue by getting similar song
# current_track = queue.pop()
# play current song
# if disliked then remove from seed_tracks and skip to next track

# request to api for audio analysis of song - WORKS
# audio_analysis = sp.audio_analysis(song_id)

print(queue)