import React from 'react';
import { render } from 'react-dom';
import CharDisplay from './CharDisplay.js';
import RadDisplay from './RadDisplay.js';
import PropTypes from 'prop-types';
import { 
    BrowserRouter as Router,
    Switch,
    Route
} from 'react-router-dom';

class App extends React.Component {

    render() {
        return (
            <Router>
                <Switch>
                    <Route 
                        exact path='/learning/display/' 
                        component={ItemDisplay} />
                </Switch>
            </Router>
        );
    }
}

class ItemDisplay extends React.Component {
    static propTypes = {
        location: PropTypes.object
    }

    renderSwitch(type, id) {
        switch (type) {
        case 'character':
            return (<CharDisplay />);
        case 'radical':
            return <RadDisplay />;
        default:
            return;
        }
    }

    render() {
        const params = new URLSearchParams(this.props.location.search);
        const type = params.get('t');
        const id = params.get('qid');
        return (
            <div className='content-card-container
            box-shadow'>
                { this.renderSwitch(type, id) }
            </div>
        );
    }
}

export default App;


