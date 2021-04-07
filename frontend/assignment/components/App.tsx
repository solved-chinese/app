import React from 'react';
import AssignmentDisplay from '@assignment.components/AssignmentDisplay';
import {LearningObjectDescriptor} from '@interfaces/CoreLearning';

export default class App extends React.Component<LearningObjectDescriptor> {

    render(): JSX.Element {
        switch (this.props.action) {
        case 'assignment':
            return <AssignmentDisplay {...this.props.content} />;
        default:
            return <>something is wrong</>;
        }
    }
}