import React from "react";
import axios from 'axios';
import './App.css';

class Base extends React.Component {
  constructor(props) {
    super(props);
    this.state = {song: "", artist: ""};
  }

  grab = async (e) => {
    e.preventDefault()
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        "song": this.state['song'],
        "artist": this.state['artist'],
      })
    };

    fetch('http://localhost:8080/play', requestOptions)
    .then(function(response) {
      console.log(response)
      return response.json()
    })
  }

  render() {
    return (
      <div className="wrapper">
        <h1>Test</h1>
        <form onSubmit={this.grab}>
            <p>
              <label>Song</label>
              <input type="text" name="song" onChange={(e) => this.setState({ song: e.target.value })}/>
              <label>Artist</label>
              <input type="text" name="artist" onChange={(e) => this.setState({ artist: e.target.value })}/>
          </p>
          <p>
              <input type="submit" value="Play" />
          </p>
        </form>
                  
      </div>        
    );
  }
}

export default Base;