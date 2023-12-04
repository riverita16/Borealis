# El Team Dream COP3530 Project 3
Alanis Rivera-Narvaez, Jorge Ramirez, David Denis

It can be hard to find songs that are similar to one specific track, rather than a broad category, artist, or genre. Spotify’s songs recommendations are sometimes unrelated, unreliable, out of place, and simply off. It is also time consuming to manually search for your next song. So users need a reliable, fast, and easier way to find new songs they like based on their preferences. A simple UI makes for minimal user interaction required but maximal satisfaction with the results.

## Borealis
- **Spotify API** application to find and listen to an infinite number of songs that are similar to just one -- personalized radio.
  - User enters one song and that is used to find similar tracks and artists
  - Create queue and Spotify music player
  - Sort the queue based on the user's audio characteristic and sorting algortihm selection
  - **Python** backend

  - For **front-end**: 
    - Show album art
    - Display song info 
    - **React JS** and **Flask** for frontend

**Note:** The program expects a song. If a different form of media is inputted, Borealis will find a song that most closely matches the entered name.

## Algorithms
- Mergesort
- Smoothsort

## Workflow
- [x] Flask interacts with React code
- [x] Front end for home page
- [x] Add characteristic and search algorithm drop downs
      - [x] Send values on submit
- [x] Spotify player renders
- [x] Queue play works
- [x] When song ends go to next song (no back function)
  - [ ] Fix multiple requests to /next at song end
- [x] Add to liked songs functionality (EDIT: Embedded player already has this functionality)
- [ ] Validate only tracks are inputted (catch fails to /track endpoint)

- [ ] Sort queue
    - [x] Mergesort
    - [ ] Smoothsort
    - [ ] Allow each by a song characteristic

- [ ] Make new logo for tab

# Dependencies
- set env vars
- requests
- selenium
- flask
- flask_cors
- npm
- react

# npm error fixes 'ERR_OSSL_EVP_UNSUPPORTED'
- export NODE_OPTIONS=--openssl-legacy-provider
