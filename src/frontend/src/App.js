import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './App.css';

function App() {
    const navigate = useNavigate();

    const [song, setSong] = useState('');
    const [artist, setArtist] = useState('');
    const [characteristic, setCharac] = useState('');
    const [sort, setSort] = useState('');

    useEffect(() => {
        // Reset the input values when the component mounts (user navigates back)
        return () => {
            setSong('');
            setArtist('');
            setCharac('');
            setSort('');
        };
    }, []);

    const Grab = async (e) => {
        e.preventDefault()
        if (!(song.trim() === '' || artist.trim() === '' || characteristic.trim() === '' || sort.trim() === '')) {
            const data = {
                song: song.trim(),
                artist: artist.trim(),
                characteristic: characteristic,
                sort: sort

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

                    <h2>Sort by...</h2>
                    <div className='dropdown'>
                        <select name="characteristic" id="characteristic" onChange={(e) => setCharac(e.target.value)}>
                            <option value="" disabled selected id="placeholder">Characteristic</option>
                            <option value="acousticness">Acousticness</option>
                            <option value="danceability">Danceability</option>
                            <option value="energy">Energy</option>
                            <option value="instrumentalness">Instrumentalness</option>
                            <option value="loudness">Loudness</option>
                            <option value="valence">Valence</option>
                            <option value="key">Key</option>
                            <option value="tempo">Tempo</option>
                        </select>

                        <select name="sorting" id="sorting" onChange={(e) => setSort(e.target.value)}>
                            <option value="" disabled selected id="placeholder">Algorithm</option>
                            <option value="merge">Merge Sort</option>
                            <option value="quick">Quick Sort</option>
                            <option value="bubble">Bubble Sort</option>
                        </select>
                    </div>

                    <button type="submit">Play</button>
                </form>
            </div>
        </div> 
    );
}

export default App;