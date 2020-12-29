import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';

export default class RadBreakdown extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            show: false
        };
    }

    // Since this function is used as event handler, use
    // arrow function to bind `this` to the class context.
    toggle = () => {
        this.setState( prev => ({show: !prev.show}));
    }

    render() {
        return (
            <div className='breakdown-container'>
                <div className='breakdown-toggle' onClick={this.toggle}>
                    <h4>
                        {(this.state.show ? 'Close' : 'Show me the') +
                            ' radical breakdown'
                        }
                    </h4>
                    <i className={
                        'fas fa-chevron-down ' + 
                        (this.state.show ? 'inversed' : '')} >
                    </i>
                </div>
            </div>
        );
    }
}