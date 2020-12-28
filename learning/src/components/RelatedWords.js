import React from 'react';
import styled from 'styled-components';
import PropTypes from 'prop-types';


/** Display related words that a user has seen. */
export default class RelatedWords extends React.Component {

    static propTypes = {
        /** The character used to look up related */
        character: PropTypes.string.isRequired
    }

    render() {
        return 'foo';
    }
}