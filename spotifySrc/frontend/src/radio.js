import React, { useEffect } from 'react';
import { Spotify } from 'react-spotify-embed'
import { useNavigate, useLocation } from 'react-router-dom'
import './radio.css';

const Radio = () => {
    const navigate = useNavigate();

    const location = useLocation();
    const { url } = location.state;

    useEffect(() => {
        console.log(url)
        if (!url) {
            navigate('/');
            return null; // You may choose to render something else while redirecting
        }
    });

    return (
        <div className='Radio'>
            <h1>Now Playing...</h1>
            <Spotify link={url} />
        </div>
    );
}

export default Radio;


// <iframe autoPlay title="Spotify Web Player" src={`https://open.spotify.com/embed${fullURL.pathname}`} width={300} height={380} allow="encrypted-media" style={{borderRadius: 0}}/>

