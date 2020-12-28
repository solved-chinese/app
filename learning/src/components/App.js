import React from 'react';
import { render } from 'react-dom';
import CharDisplay from './CharDisplay.js';

class App extends React.Component {


    render() {
        return (
            <CharDisplay />
        );
    }
}

export default App;

const container = document.getElementById('learning-app');
render(<App />, container);
