import React from 'react';
import { render } from 'react-dom';
import CharDisplay from './CharDisplay.js';
import RadDisplay from './RadDisplay.js';
import { 
    BrowserRouter as Router,
    Switch,
    Route
} from 'react-router-dom';

class App extends React.Component {

    render() {
        return (
            <Router>
                <div className='content-card-container 
                box-shadow'>
                    {/* <RadDisplay /> */}
                    <CharDisplay />
                </div>
            </Router>
        );
    }
}

export default App;


