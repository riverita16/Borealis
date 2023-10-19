import React from 'react';
import './App.css';
// import { useNavigate } from 'react-router-dom'
// import Radio from './radio';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {song: "", artist: ""};
    this.navigate = '/radio';
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

    fetch('/start', requestOptions)
    .then(response => response.json())
    .then(data => {
        // TODO: validate response
        console.log(data)
        // WithNavigate(this.props)
        return(
          <div>hello</div>
        );
        // const url = new URL(data['url']);
    })
  }

  render() {
    return (
      <div>
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

// export function WithNavigate(props) {
//   let navigate = useNavigate()
//   return <App {...props} navigate = {navigate} />
// }

export default App;