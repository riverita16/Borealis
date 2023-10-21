import React, { useState, useEffect, useCallback } from 'react';
import { Spotify } from 'react-spotify-embed'
import { useNavigate, useLocation } from 'react-router-dom'
import './radio.css';

const Radio = () => {
    // let canvas = document.getElementById("audio_visual");
    // let ctx = canvas.getContext("2d");
    const navigate = useNavigate();

    const location = useLocation();
    const { url } = location.state;
    const [updatedUrl, setUrl] = useState(url);
    const [playback, setPlay] = useState('pause');

    const [btn_class, setClass] = useState('add');
    const [text, setText] = useState('+')

    useEffect(() => {
        // Reset the playback value when the component mounts (user navigates back)
        return () => {
            setPlay('pause');
        };
    }, []);

    useEffect(() => {
        console.log(url)
        if (!url) {
            navigate('/');
            return null; // You may choose to render something else while redirecting
        }
    });

    // switch to next song in queue
    const Next = useCallback(async (e) => {
        e.preventDefault()

        const response = await fetch('/next', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
        });

        if (response.ok) {
            const responseData = await response.json();
            console.log(responseData.url)
            setUrl(responseData.url);
            setClass('add')
            setText('+')
        } else {
            alert("Error occurred while fetching data");
        }
    }, []);

    // track user pause and play for visualizer
    useEffect(() => {
        window.addEventListener(
            "message",
            (event) => {
                if (event.origin !== "https://open.spotify.com") return;

                if (event.data.type === 'playback_update') {
                    setPlay((prevState) => {
                        if (prevState === 'pause' && !event.data.payload.isPaused) {
                            console.log('play')
                            return 'play'
                        } else if (prevState === 'play' && event.data.payload.isPaused) {
                            // when song ends go to next song
                            if (parseInt(event.data.payload.position) === 0) {
                                console.log('Song ended')
                                const syntheticEvent = {
                                    preventDefault: () => {}
                                }

                                Next(syntheticEvent)
                                return prevState

                            } else console.log('paused')
                            
                            return 'pause'
                        }
    
                        return prevState
                    });

                    // console.log(parseInt(event.data.payload.position / 1000, 10) + ' : ' + parseInt(event.data.payload.duration / 1000, 10))
                
                } else if (event.data.type === 'ready') {
                    console.log('Song loaded')

                    // automatically start song if it was switched to automatically
                    if (playback === 'play') {
                        const spotifyEmbedWindow = document.querySelector('iframe[src*="https://open.spotify.com"]').contentWindow;
                        spotifyEmbedWindow.postMessage({command: 'toggle'}, '*');
                    }
                }

                else console.log(event.data)
            },
            false,
        );

        // return () => {
        //     window.removeEventListener('message', handleIframeEvent);
        // };
    }, [Next, playback]);

    // add to user liked songs
    const Like = async (e) => {
        e.preventDefault()

        setClass('added')
        setText('Added')

        const response = await fetch('/like', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
        });

        if (response.ok) {
            console.log('added song to library')
        } else {
            alert("Error occurred while putting data");
        }
    }

    return (
        <div className='Radio'>
            <h1>Now Playing...</h1>

            <div id="transparent">
                <Spotify link={updatedUrl} />
            </div>
            <div>
                <button className={btn_class} onClick={Like}>{text}</button>
                <button id="next" onClick={Next}>Next Song</button>
            </div>
        </div>
    );
}

export default Radio;


// <iframe autoPlay title="Spotify Web Player" src={`https://open.spotify.com/embed${fullURL.pathname}`} width={300} height={380} allow="encrypted-media" style={{borderRadius: 0}}/>

// analyzer will go in  <canvas id="audio_visual"></canvas> 
