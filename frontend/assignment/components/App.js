import React from 'react';
import PropTypes from 'prop-types';
import AssignmentDisplay from "@assignment.components/AssignmentDisplay";


export default class App extends React.Component {
    static propTypes = {
        action: PropTypes.string.isRequired,

        content: PropTypes.object.isRequired
    }

    render() {
        switch (this.props.action) {
            case 'assignment':
                return <AssignmentDisplay {...this.props.content} />;
            default:
                return "something is wrong";
        }
    }
}