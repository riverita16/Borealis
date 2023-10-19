import React, { useState } from 'react';
import { Route, Routes, useNavigate } from 'react-router-dom';
import Radio from './radio';
import './App.css';

function App() {
    const navigate = useNavigate();

    const [url, setUrl] = useState('');
    const [song, setSong] = useState('');
    const [artist, setArtist] = useState('');

    const Grab = async (e) => {
        e.preventDefault()

        const data = {
            song: song,
            artist: artist
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
            setUrl(responseData.url);
            navigate('/radio')
        } else {
            alert('Error occurred while fetching data');
        }
    };

    return (
        <div className="App">
            <Routes>
                <Route path='/' element= {
                    <div>
                        <h1>Test</h1>
                        <form onSubmit={Grab}>
                            <label>Song</label>
                            <input
                                type="text"
                                value={song}
                                onChange={(e) => setSong(e.target.value)}
                            />
                            <label>Artist</label>
                            <input
                                type="text"
                                value={artist}
                                onChange={(e) => setArtist(e.target.value)}
                            />
                            <button type="submit">Submit</button>
                        </form>
                        {url && <p>Received URL: {url}</p>}
                    </div>
                } />

                <Route path="/radio" element={ <Radio url={url} />} />
            </Routes>
        </div> 
    );
}

export default App;