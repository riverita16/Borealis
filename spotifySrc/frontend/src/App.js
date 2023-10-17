import React from 'react';
import { createRoot } from 'react-dom/client';
import Spotify from 'react-spotify-embed/dist/package.json'
import { Container } from 'react-bootstrap'
import './App.css';

// function Iframe(props) {
//   return (<div dangerouslySetInnerHTML={ {__html:  props.iframe?props.iframe:""}} />);
// }

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

    await fetch('/start', requestOptions)
    .then(function(response) {
      console.log(response.json())
      const url = new URL(response['url']);
      // const spotify = "<Spotify link={response.json()['url']} />"
      // const iframe = '<iframe title="Spotify Web Player" src={`https://open.spotify.com/embed${url.pathname}`} width={300} height={380} allow="encrypted-media" style={{borderRadius: 8}}/>'
      return (
        <div>
          <Container>
            <h1>Iframe Demo</h1>
            <iframe title="Spotify Web Player" src={`https://open.spotify.com/embed${url.pathname}`} width={300} height={380} allow="encrypted-media" style={{borderRadius: 8}}/>
          </Container>
        </div>
      );
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

// const rootElement = document.getElementById("root");
// const root = createRoot(rootElement);
// root.render(<Base />);

export default Base;