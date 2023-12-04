import React, { useState, useEffect, useCallback } from 'react';
import { Spotify } from 'react-spotify-embed'
import { useNavigate, useLocation } from 'react-router-dom'
import './radio.css';

const Radio = () => {
    const navigate = useNavigate();

    const location = useLocation();
    const { url } = location.state;
    const [updatedUrl, setUrl] = useState(url);
    const [playback, setPlay] = useState('pause');

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
        } else {
            alert("Error occurred while fetching data");
        }
    }, []);

    const checkEnd = async () => {

    }
    
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
                            // FIX MULTIPLE GET REQUESTS
                            console.log(event.data.payload.position)
                            if (parseFloat(event.data.payload.position) === 0.0) {
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

    return (
        <div className="Radio aurora-outer">
            <section id="up" />
            <section id="down" />
            <section id="left" />
            <section id="right" />
            <div className="box stuff">
                <h1>Now Playing...</h1>

                <div id="transparent">
                    <Spotify link={updatedUrl} />
                </div>
                <div>
                    <button id="next" onClick={Next}>Next Song</button>
                </div>
            </div>
        </div>
    );
}

export default Radio;