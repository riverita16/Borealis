import React, { useState, useEffect } from "react";
import axios from 'axios';
import './App.css';

function App() {
  const grab = (e) => {
    e.preventDefault();
    axios
        .post("/start", {
            song: document.getElementById("song").value,
            artist: document.getElementById("artist").value,
        })
        .then((res) => {
            // display embedded spotify player
            return res.json().then( (data) => console.log(data));
        });
  }
  return(
    <div className="wrapper">
      <h1>Test</h1>
      <form onSubmit={grab} method="post">
          <p>
            <label htmlFor="song">Song</label>
            <input type="song" className="w3-input w3-border" id="song" name="song" />
            <label htmlFor="artist">Artist</label>
            <input type="artist" className="w3-input w3-border" id="artist" name="artist" />
        </p>
        <p>
            <input type="submit" className="w3-button w3-blue" value="Play" />
        </p>
      </form>
                
    </div>        
  );
}

export default App;