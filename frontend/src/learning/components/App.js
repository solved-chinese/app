import React from 'react';

import ItemDisplay from './ItemDisplay/ItemDisplay.js';
import ReviewQuestion from './ReviewQuestion/ReviewQuestion.js';


export default class App extends React.Component {

    render() {
        switch (this.props.action) {
            case 'display':
                return <ItemDisplay {...this.props.content} />;
            case 'review':
                return <ReviewQuestion {...this.props.content} />;
            default:
                return;
        }
    }
}
