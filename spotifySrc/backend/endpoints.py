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

from spot import Spot
from radio import Radio
from flask import Flask, jsonify, request, redirect
from flask_cors import CORS

HOST_IP_ADDRESS = 'localhost'
HOST_PORT = '8080'

# Env vars
# USERNAME = os.environ['SpotifyUser']
CLIENT_ID = os.environ.get('BorealisCID')
CLIENT_SECRET = os.environ.get('BorealisSecret')

SCOPE = 'playlist-modify-private playlist-modify-public'
REDIRECT_URI = 'http://localhost:8080/callback'

app = Flask('Borealis')
CORS(app)

'''
Test env vars can be read (for mac in ~/.zshenv)
print(CLIENT_ID)
print(CLIENT_SECRET)
'''

spot = Spot(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
radio = Radio(spot) 

@app.route('/start', methods=['POST'])
def start():
    # grab user front-end 
    response = request.get_json()
    radio.start_song = response['song']
    radio.start_artist = response['artist']
    
    # authenticate with api
    spot.authorize(SCOPE) 

    return {'status':200}

@app.route('/callback')
def callback():
    code = request.args.get('code')
    credentials = spot.get_token(code)
    spot.ACCESS_TOKEN = credentials['access_token']

    spot.get_profile()

    song_id = radio.generate()
    # visualize = spot.audio_analysis(song_id) # implement

    # return oEmbed API response for spotify player and visuals
    return {'url':radio.songEmbed(song_id)['url']}

@app.route('/upNext', methods=['GET'])
def upNext():
    return jsonify(next=radio.queue[-1])

# return player html for next song
@app.route('/next', methods=['GET'])
def next():
    song_id = radio.queue.pop()
    radio.seed_tracks.add(song_id)
    url = radio.songEmbed(song_id)['url']
    # visualizer = SP.audio_analysis(song_id) #implement

    return {'url':url}

@app.route('/action', methods=['POST'])
def action():
    act = request.args['action']
    song_id = request.args['song_id']
    if act == 'dislike':
        # re-generate queue
        radio.seed_tracks.discard(song_id)
        radio.resetQueue()
        return next()
    else:
        # add to user spotify library
        pass

if __name__ == '__main__':
    app.run(host=HOST_IP_ADDRESS, port=HOST_PORT, use_reloader=True, debug=True)