import React from 'react';
import 'core-js/stable';
import 'regenerator-runtime/runtime';
import PropTypes from 'prop-types';
import styled from 'styled-components';

import CharDefinition from './CharDefinition.js';

import RelatedItems from '@learning.components/ItemDisplay/RelatedItems.js';
import ItemPhonetic from '@learning.components/ItemDisplay/ItemPhonetic.js';
import BreakdownView from '@learning.components/ItemDisplay/BreakdownView';
import LoadingView from '@learning.components/ItemDisplay/LoadingView.js';

import useLoadChar from '@learning.hooks/useLoadChar.js';

const Row = styled.div`
    display: flex;
    justify-content: center;
    align-items: center;
    @media only screen and (max-width: 480px) {
        flex-direction: column;
    }
`;

/** The main function that renders a character view. */
export default function CharDisplay(props) {

    const character = useLoadChar(`/content/character/${props.qid}`);

    const renderCharacter = (character) => {
        const definitions = character.definitions.map( v => 
            v.definition
        );
        return (
            <>
                <Row>
                    <ItemPhonetic pinyin={character.pinyin}
                        audioURL=''
                        item={character.chinese}/>
                    <CharDefinition 
                        definitions={ definitions }
                    />
                </Row>
                <RelatedItems 
                    item={character.chinese}
                    itemType='word' />
                <BreakdownView type='radical'
                    componentURL={character.radicals}
                    memoryAid={character.memory_aid}/>
            </>
        );
    };

    if (character === null) {
        return <LoadingView />;
    } else {
        return renderCharacter(character);
    }
}

CharDisplay.propTypes = {
    qid: PropTypes.number
};