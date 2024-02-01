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
    - **React JS** and **Flask**

- [Demo](https://youtu.be/8d2Dl2nf7Qg)

**Notes:** 
- The program expects a song. If a different form of media is inputted, Borealis will find a song that most closely matches the entered name.
- The program CSS is based on Chrome. Ensure this is your default browser.

## Getting Started
1. Set the Client ID and Client Secret environment variables as per `src/backend/endpoints.py`
2. Within `src/backend` run `python3 endpoints.py` to start **Flask** server on the localhost
3. Within `src/frontend` run `npm run`
4. Enter song name and artist
5. Select sorting algorithm and characteristic
6. Enter or click "Play"
7. On newly opened window, sign into Spotify account (ensure user is whitelisted)
8. Go back to original browser to continue using the program

## Algorithms
- Merge Sort
- Quick Sort
- Bubble Sort

## Workflow
- [x] Flask interacts with React code
  - [x] Fixed returning to '/' endpoint and doing new runs
- [x] Front end for home page
  - [x] Prevent form submit without all components set
- [x] Add characteristic and search algorithm drop downs
  - [x] Send values on submit
- [x] Spotify player renders
- [x] Queue play works
  - [x] Fixed for endless queue no repeats
  - [x] Fixed potental api error if # of seeds exceeded 5
- [x] When song ends go to next song (no back function)
  - [x] Fix multiple calls to Next in auto queue
- [x] Add to liked songs functionality (EDIT: Embedded player already has this functionality)
- [x] Added Home button
- [x] Fixed multiple authentications in same runs if start song changed
- [x] Fix access token expiration -- check time change and re-auth with refresh token

- [x] Sort queue
  - [x] Merge Sort
  - [x] Quick Sort
  - [x] Bubble Sort
  - [x] Allow each by a song characteristic
  - [x] Execution comparisons

- [x] Add feature that adds played songs to .txt file for future reference
  - [x] Do not push this file (add to .gitignore)
  - [x] Fix trailing comma
  - [x] Add session info before appending songs
  - [ ] Supplemental program to help parse these
    - [ ] Add link to each song to help user

- [ ] Further `songs.txt` functionality
  - [ ] Add switch to control whether the session is being written to the file

## Dependencies
- Spotify Developer account
- Set environment vars / Client ID and Secret
- python3
- Installed with **pip3**
  - requests
  - selenium
  - flask
  - flask_cors
  - npm
  - react
- Ran `npm install` for rest of node_modules

### npm error fixes 'ERR_OSSL_EVP_UNSUPPORTED'
- `export NODE_OPTIONS=--openssl-legacy-provider`
