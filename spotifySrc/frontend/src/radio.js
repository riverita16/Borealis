import React, { useState, useEffect } from 'react';
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

    useEffect(() => {
        console.log(url)
        if (!url) {
            navigate('/');
            return null; // You may choose to render something else while redirecting
        }
    });

    const Next = async (e) => {
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
    }

    return (
        <div className='Radio'>
            <h1>Now Playing...</h1>

            <div id="transparent">
                <Spotify link={updatedUrl} />
            </div>
            <div>
                <button onClick={Next}>Next Song</button>
            </div>
        </div>
    );
}

export default Radio;


// <iframe autoPlay title="Spotify Web Player" src={`https://open.spotify.com/embed${fullURL.pathname}`} width={300} height={380} allow="encrypted-media" style={{borderRadius: 0}}/>

// analyzer will go in  <canvas id="audio_visual"></canvas> 
