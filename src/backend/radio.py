from spot import Spot
from flask import jsonify
from mergesort import merge_sort
from quicksort import quick_sort
from bubblesort import bubble_sort
from time import time
from datetime import datetime

# generate radio queue by getting similar song

class Radio:
    def __init__(self, sp) -> None:
        self.queue = []
        self.played = set() # played song ids
        self.spot = sp

        # associated with initial song
        self.seed_genres = set()
        self.seed_artists = set()

    start_song = ''
    start_artist = ''
    start_id = ''
    curr_id = ''

    # for sorting
    characteristic = ''
    sort_alg = ''

    # reset all sets and arrays for subsequent runs
    def clear_all(self):
        self.queue.clear()
        self.played.clear()
        self.seed_genres.clear()
        self.seed_artists.clear()

    # return HTML to embed player
    def song_embed(self, song_id):
        self.played.add(song_id)
        # get song id spotify url
        curr_url = self.spot.request('https://api.spotify.com/v1/tracks/'+song_id, {})['external_urls']['spotify']
        return {'url':curr_url}

    # generate queue
    def generate(self, newStart=False):
        # first queue generation
        if newStart:
            self.clear_all()

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

            # Prevent api errors with more than 5 seeds
            while (len(self.seed_artists) + len(self.seed_genres) > 4):
                self.seed_artists.pop()

            while (len(self.seed_artists) + len(self.seed_genres) > 4):
                self.seed_genres.pop()
            
            # append session info
            with open('../../songs.txt', 'a+') as songs:
                name = song['name']
                artists = song['artists']
                current_time = datetime.now()
                append_str = f'\nSession started on {current_time.date()} at {current_time.hour}:{current_time.minute}:{current_time.second} with "{name}" by '
                
                for artist in artists:
                    append_str += artist['name'] + ', '

                append_str = append_str[:-2] # trailing commas

                songs.write(append_str + '\n')

        # all calls to queue generation
        tracks = self.spot.request('https://api.spotify.com/v1/recommendations?', {'limit':100, 'seed_artists':self.seed_artists, 'seed_genres':self.seed_genres, 'seed_tracks':self.start_id, 'country':'US'})['tracks']
        
        for track in tracks:
            if track['id'] not in self.played: # no repeats
                self.queue.append({'id': track['id'], 'url': track['external_urls']['spotify']})

        # print(self.queue)
        self.sort()

        return self.start_id
    

    def write_song(self, id):
        with open('../../songs.txt', 'a+') as songs:
            track = self.spot.request('https://api.spotify.com/v1/tracks/'+id, {})
            name = track['name']
            artists = track['artists']
            append_str = f'"{name}" by '
            
            for artist in artists:
                append_str += artist['name'] + ', '

            append_str = append_str[:-2] # trailing commas

            songs.write(append_str + '\n')


    # ids is string of comma-separated ids
    def analyze(self, ids, charac):
        characs = []
        response = self.spot.request(f'https://api.spotify.com/v1/audio-features?', {'ids':ids})['audio_features']
        # print(response)

        for track in response:
            characs.append({'id':track['id'], 'url':f'https://open.spotify.com/track/'+track['id'], charac:track[charac]})

        return characs

    def sort(self):
        if self.sort_alg == '' or self.characteristic == '':
            return # do nothing
        
        # get start song characteristic
        start_charac = self.analyze(self.start_id, self.characteristic)[0][self.characteristic]

        # get tuple array of queue with characteristic value
        ids = ''
        for track in self.queue:
            ids += track['id'] + ','

        ids = ids[:-1] # remove extra comma
        print(ids)

        # queue now has characteristics for each track
        self.queue = self.analyze(ids, self.characteristic)

        # make characs the difference between the value and the start value
        for track in self.queue:
            track[self.characteristic] = abs(start_charac - track[self.characteristic])

        # sort self.queue based on start_charac value
        if self.sort_alg == 'merge':
            start_time = time()
            merge_sort(self.queue, self.characteristic)
            end_time = time()
            print(f'Merge Sort took {end_time - start_time} seconds')
        elif self.sort_alg == 'quick': 
            start_time = time()
            quick_sort(self, 0, len(self.queue) - 1)
            end_time = time()
            print(f'Quick Sort took {end_time - start_time} seconds')
        else:
            start_time = time()
            bubble_sort(self)
            end_time = time()
            print(f'Bubble Sort took {end_time - start_time} seconds')