import React from 'react';
import PropTypes from 'prop-types';

import CharDisplay from './CharDisplay.js';
import WordDisplay from './WordDisplay.js';
import RadDisplay from './RadDisplay.js';

export default class ItemDisplay extends React.Component {
    
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