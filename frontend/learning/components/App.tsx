import React from 'react';

import ItemDisplay from './ItemDisplay/ItemDisplay';
import ReviewQuestion from './ReviewQuestion/ReviewQuestion';
import CoreLearning from './CoreLearning/CoreLearning';
import SearchPage from "@learning.components/SearchPage";
import {ItemType} from '@interfaces/CoreItem';

type Props = {
    action: 'display' | 'review' | 'learning' | 'search',
    content: any
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
            case "search":
                return <SearchPage {...this.props.content} />;
            default:
                return <>`Error: no such action {this.props.action}`</>;
        }
    }
}
