from spot import Spot
from flask import jsonify
import mergesort

# generate radio queue by getting similar song

class Radio:
    def __init__(self, sp) -> None:
        self.queue = []
        self.played = set() # played song ids
        self.spot = sp

        # associated with initial song
        self.seed_genres = set()
        self.seed_artists = set ()

    start_song = ''
    start_artist = ''
    start_id = ''
    curr_id = ''

    # for sorting
    characteristic = ''
    sort = ''

    # return HTML to embed player
    def songEmbed(self, song_id):
        self.played.add(song_id)
        # get song id spotify url
        curr_url = self.spot.request('https://api.spotify.com/v1/tracks/'+song_id, {})['external_urls']['spotify']
        return {'url':curr_url}

    # generate queue
    def generate(self):
        # first queue generation
        if self.start_id == '':
            song = self.spot.request('https://api.spotify.com/v1/search?', {'q':f'track:{self.start_song} artist:{self.start_artist}', 'type':'track', 'limit':1})['tracks']['items']
            if len(song) == 0:
                song = self.spot.request('https://api.spotify.com/v1/search?', {'q':f'{self.start_song} {self.start_artist}', 'type':'track', 'limit':1})['tracks']['items']

            song = song[0]
            self.start_id = song['id']
            self.now_playing = self.start_id
            self.played.add(self.start_id)

            for artist in song['artists']:
                self.seed_artists.add(artist['id'])
                if 'genres' in artist:
                    self.seed_genres.update(artist['genres'])

        # all calls to queue generation
        tracks = self.spot.request('https://api.spotify.com/v1/recommendations?', {'limit':100, 'seed_artists':self.seed_artists, 'seed_genres':self.seed_genres, 'seed_tracks':self.played, 'country':'US'})['tracks']
        
        for track in tracks:
            self.queue.append({'id': track['id'], 'url': track['external_urls']['spotify']})

        # self.sort()
        print(self.queue)

        return self.start_id
    
    # ids is string of comma-separated ids
    def analyze(self, ids, charac):
        characs = []
        response = self.spot.request('https://api.spotify.com/v1/audio-features?', {'ids':ids})['audio_features']
        for track in response:
            characs.append({'id':track['id'], 'url':f'https://open.spotify.com/track/'+track['id'], charac:track[charac]})

        return characs

    def sort(self):
        if self.sort == '' or self.characteristic == '':
            return # do nothing
        
        # get start song characteristic
        start_charac = self.analyze(self.start_song, self.characteristic)[self.characteristic]

        # get tuple array of queue with characteristic value
        ids = ''
        for track in self.queue:
            ids += track['id'] + ','

        ids = ids[:-1] # remove extra comma

        # queue now has characteristics for each track
        self.queue = self.analyze(ids, self.characteristic)

        # sort self.queue based on start_charac value
        if self.sort == 'merge':
            pass # mergesort
        else: # quicksort
            pass