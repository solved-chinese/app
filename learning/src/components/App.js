import React from 'react';
import { render } from 'react-dom';
import CharDisplay from './CharDisplay.js';
import RadDisplay from './RadDisplay.js';
import WordDisplay from './WordDisplay.js';
import PropTypes from 'prop-types';
import { 
    BrowserRouter as Router,
    Switch,
    Route
} from 'react-router-dom';



export default class App extends React.Component {


    render() {
        return (
            <WordDisplay qid={42} />
            
            // <Router>
            //     <Switch>
            //         <Route 
            //             exact path='/learning/display/' 
            //             component={ItemDisplay} />
            //     </Switch>
            // </Router>
        );
    }
}

class ItemDisplay extends React.Component {
    static propTypes = {
        location: PropTypes.object
    }

    renderSwitch(type, qid) {
        switch (type) {
        case 'character':
            return (<CharDisplay qid={qid} />);
        case 'radical':
            return <RadDisplay qid={qid} />;
        case 'word':
            return <WordDisplay qid={qid} />;
        default:
            return ;
        }
    }

    render() {
        const params = new URLSearchParams(this.props.location.search);
        const type = params.get('t');
        const qid = parseInt(params.get('qid'), 10);
        return (
            <div className='content-card-container
            box-shadow'>
                { this.renderSwitch(type, qid) }
            </div>
        );
    }
}

