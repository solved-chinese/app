import React from 'react';
import styled from 'styled-components';

import '@learning.styles/ItemDisplay.css';

const DefinitionList = styled.ul`

    padding-left: 70px;
    font-size: 1.3em;

    @media only screen and (max-width: 480px) {
        padding: 0;
    }
`;

const ListTitle = styled.i`
    font-size: 0.6em;
    font-style: normal;
    color: var(--teritary-text);
    line-height: 1em;
`;

const ListItem = styled.li`
    line-height: 1.75em;
`;

type Props = {
    /** The definitions to be displayed */
    definitions: string[]
}

const CharDefinition = (props: Props): JSX.Element => {
    return (
        <DefinitionList>
            <ListTitle>Definitions:</ListTitle>
            {props.definitions.map( (elem, i) => {
                return (
                    <ListItem key={i} className='use-serifs'> 
                        {elem} 
                    </ListItem>
                );
            })}
        </DefinitionList>
    );
};

export default CharDefinition;