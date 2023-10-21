from spot import Spot
from flask import jsonify

# generate radio queue by getting similar song
# current_track = queue.pop()
# play current song
# if disliked then remove from seed_tracks and skip to next track

# request to api for audio analysis of song - WORKS
# audio_analysis = sp.audio_analysis(song_id)

class Radio:
    def __init__(self, sp) -> None:
        self.queue = []
        self.seed_tracks = set() # used to generate recs
        self.played = set() # played song ids
        self.spot = sp

    start_song = ''
    start_artist = ''
    curr_id = ''
    curr_url = ''
    now_playing = ''

    # return HTML to embed player
    def songEmbed(self, song_id):
        self.played.add(song_id)
        # get song id spotify url
        curr_url = self.spot.request('https://api.spotify.com/v1/tracks/'+song_id, {})['external_urls']['spotify']
        return {'url':curr_url}

    # generate queue
    def generate(self):
        current_track = self.spot.request('https://api.spotify.com/v1/search?', {'q':f'track:{self.start_song} artist:{self.start_artist}', 'type':'track', 'limit':1})['tracks']['items']
        if len(current_track) == 0:
            current_track = self.spot.request('https://api.spotify.com/v1/search?', {'q':f'{self.start_song} {self.start_artist}', 'type':'track', 'limit':1})['tracks']['items']

        current_track = current_track[0]
        song_id = current_track['id']
        self.now_playing = song_id
        self.played.add(song_id)
        artist_ids = set()
        genres = set()

        for artist in current_track['artists']:
            artist_ids.add(artist['id'])
            if 'genres' in artist:
                genres.update(artist['genres'])

        tracks = self.spot.request('https://api.spotify.com/v1/recommendations?', {'seed_artists':artist_ids, 'seed_genres':genres, 'seed_tracks':self.seed_tracks, 'country':'US'})['tracks']
        
        for track in tracks:
            self.queue.append({'id': track['id'], 'url': track['external_urls']['spotify']})

        print(self.queue)

        return song_id

    def resetQueue(self):
        self.queue = self.spot.request('https://api.spotify.com/v1/recommendations?', {'seed_tracks':self.seed_tracks, 'country':'US'})['tracks']
