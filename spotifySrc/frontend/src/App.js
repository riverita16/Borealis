import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './App.css';

function App() {
    const navigate = useNavigate();

    const [song, setSong] = useState('');
    const [artist, setArtist] = useState('');

    useEffect(() => {
        // Reset the input values when the component mounts (user navigates back)
        return () => {
            setSong('');
            setArtist('');
        };
    }, []);

    const Grab = async (e) => {
        e.preventDefault()
        if (!(song.trim() === '' || artist.trim() === '')) {
            const data = {
                song: song.trim(),
                artist: artist.trim()
            };
    
            const response = await fetch('/start', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
    
            if (response.ok) {
                const responseData = await response.json();
                console.log(responseData)
    
                navigate('/radio', { state: { url: responseData.url } });
            } else {
                alert("Error occurred while fetching data");
            }
        }
    };

    return (
        <div className="App aurora-outer">
            <section id="up" />
            <section id="down" />
            <section id="left" />
            <section id="right" />
            <div className="box stuff">
                <h1>Borealis</h1>
                <form onSubmit={Grab}>
                    <input
                        type="text"
                        value={song}
                        placeholder='Song'
                        onChange={(e) => setSong(e.target.value)}
                    />
                    <input
                        type="text"
                        value={artist}
                        placeholder='Artist'
                        onChange={(e) => setArtist(e.target.value)}
                    />
                    <button type="submit">Play</button>
                </form>
            </div>
        </div> 
    );
}

export default App;