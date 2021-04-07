import React from 'react';

import ItemDisplay from './ItemDisplay/ItemDisplay';
import ReviewQuestion from './ReviewQuestion/ReviewQuestion';
import CoreLearning from './CoreLearning/CoreLearning';
import {ItemType} from '@interfaces/CoreItem';

type Props = {
    action: 'display' | 'review' | 'learning',
    content: {
        qid: number,
        type?: ItemType
    },
}

export default class App extends React.Component<Props> {

    render(): JSX.Element {
        switch (this.props.action) {
        case 'display':
            return <ItemDisplay
                qid={this.props.content.qid}
                type={this.props.content.type!}
            />;
        case 'review':
            return <ReviewQuestion {...this.props.content} />;
        case 'learning':
            return <CoreLearning {...this.props.content} />;
        }
    }
}
