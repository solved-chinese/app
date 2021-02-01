import React from 'react';
import PropTypes from 'prop-types';

import CharDisplay from './CharacterDisplay/CharDisplay';
import WordDisplay from './WordDisplay/WordDisplay';
import RadDisplay from './RadicalDisplay/RadDisplay';
import ProgressBar from './ProgressBar'

import '@learning.styles/ItemDisplay.css';

export default class ItemDisplay extends React.Component {
    
    static propTypes = {
        location: PropTypes.object,
        type: PropTypes.string,
        qid: PropTypes.number,
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
        return (
            <>
                <ProgressBar 
                    mastered={6}
                    familiar={11}
                    remaining={10}
                    bonus={2}
                />
                <div className='content-card-container
                box-shadow'>
                    { this.renderSwitch(this.props.type, this.props.qid) }
                </div>
            </>
        );
    }
}