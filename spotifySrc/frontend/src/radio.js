import React from 'react';
import { Spotify } from 'react-spotify-embed'
import { useNavigate } from 'react-router-dom'
import './radio.css';

const Radio = ({ url }) => {
    const navigate = useNavigate();

    if (!url) {
        navigate('/');
        return null; // You may choose to render something else while redirecting
    }

    return (
        <div>
            <h1>Spotify Player</h1>
            <Spotify link={url} />
        </div>
    );
}

export default Radio;


// <iframe autoPlay title="Spotify Web Player" src={`https://open.spotify.com/embed${fullURL.pathname}`} width={300} height={380} allow="encrypted-media" style={{borderRadius: 0}}/>

