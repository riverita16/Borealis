import os
from spot import Spot
from radio import Radio
from flask import Flask, jsonify, request
from flask_cors import CORS

HOST_IP_ADDRESS = 'localhost'
HOST_PORT = '8080'

# Env vars
CLIENT_ID = os.environ.get('BorealisCID')
CLIENT_SECRET = os.environ.get('BorealisSecret')

SCOPE = 'user-library-read user-library-modify'
REDIRECT_URI = 'http://localhost:8080/start'

app = Flask('Borealis')
CORS(app)

'''
Test env vars can be read (for mac in ~/.zshenv)
print(CLIENT_ID)
print(CLIENT_SECRET)
'''

spot = Spot(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
radio = Radio(spot) 

@app.route('/start', methods=['POST', 'GET'])
def start():
    if spot.callback is False:
        print(request.get_json()) # remove this
        # grab user front-end 
        response = request.get_json()
        radio.start_song = response['song']
        radio.start_artist = response['artist']
        radio.characteristic = response['characteristic']
        radio.sort = response['sort']
        
        # authenticate with api
        spot.authorize(SCOPE)
        # wait for data
        while radio.curr_id == '':
            continue
    else:
        callback()
        spot.callback = False

    # return oEmbed API response for spotify player and visuals
    ret = radio.songEmbed(radio.curr_id)['url']
    radio.curr_id = ''
    spot.close_browser()
    return {'url':ret}

def callback():
    code = request.args.get('code')
    credentials = spot.get_token(code)
    spot.ACCESS_TOKEN = credentials['access_token']

    spot.get_profile()

    radio.curr_id = radio.generate()
    print(radio.curr_id)

@app.route('/upNext', methods=['GET'])
def upNext():
    return jsonify(next=radio.queue[-1])

# return player html for next song
@app.route('/next', methods=['GET'])
def next():
    print(len(radio.queue)) # FOR TESTING
    track = radio.queue.pop()
    radio.played.add(track['id'])

    if len(radio.queue) == 0:
        radio.generate()

    return {'url':track['url']}

if __name__ == '__main__':
    app.run(host=HOST_IP_ADDRESS, port=HOST_PORT, use_reloader=True, debug=True)