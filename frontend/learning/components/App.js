import React from 'react';
import PropTypes from 'prop-types';

import ItemDisplay from './ItemDisplay/ItemDisplay';
import ReviewQuestion from './ReviewQuestion/ReviewQuestion';
import CoreLearning from './CoreLearning/CoreLearning';


export default class App extends React.Component {

    static propTypes = {
        action: PropTypes.string.isRequired,

        content: PropTypes.object.isRequired
    }

    render() {
        switch (this.props.action) {
        case 'display':
            return <ItemDisplay {...this.props.content} />;
        case 'review':
            return <ReviewQuestion {...this.props.content} />;
        case 'learning':
            return <CoreLearning {...this.props.content} />;
        default:
            return;
        }
    }
}
