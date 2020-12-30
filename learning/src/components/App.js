import React from 'react';
import { render } from 'react-dom';
import CharDisplay from './CharDisplay.js';
import RadDisplay from './RadDisplay.js';

class App extends React.Component {


    render() {
        return (
            <div className='content-card-container 
                box-shadow'>
                {/* <RadDisplay /> */}
                <CharDisplay />
            </div>
        );
    }
}

export default App;

const container = document.getElementById('learning-app');
render(<App />, container);
