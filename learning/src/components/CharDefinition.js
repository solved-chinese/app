import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';

const Container = styled.div`
    display: inline-flex;
    flex-direction: column;
    align-self: flex-start;
    @media only screen and (max-width: 768px) {
        align-self: center;
    }
`;

export default function CharDefinition(props) {
    return (
        <Container>
            <ul className='definition-list'>
                <i>Definitions:</i>
                {props.definitions.map( (elem, i) => {
                    return (
                        <li key={i} className='use-serifs'> 
                            {elem} 
                        </li>
                    );
                })}
            </ul>
        </Container>
    );
}

CharDefinition.propTypes = {
    /** The definitions to be displayed */
    definitions: PropTypes.arrayOf(
        PropTypes.string
    ) 
};