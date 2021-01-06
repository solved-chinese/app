import React from 'react';
import { 
    BrowserRouter as Router,
    Switch,
    Route
} from 'react-router-dom';

import ItemDisplay from './ItemDisplay/ItemDisplay.js';

export default class App extends React.Component {

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

