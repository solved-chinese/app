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

    const character = useLoadChar( 
        props.url == null ?
            `/content/character/${props.qid}` :
            props.url
    );

    const renderCharacter = (character) => {
        const definitions = character.definitions.map( v => 
            v.definition
        );
        return (
            <>
                <Row>
                    <ItemPhonetic pinyin={character.pinyin}
                        audioURL={character.audio}
                        item={character.chinese}/>
                    <CharDefinition 
                        definitions={ definitions }
                    />
                </Row>
                <RelatedItems 
                    items={character.related_words}
                    item={character.chinese}
                    itemType='character' />
                <BreakdownView type='radical'
                    componentURL={character.radicals}
                    memoryAid={character.memory_aid}
                    alwaysDisplay={props.alwaysDisplay}
                />
                    
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
    /** The URL of the character to be rendered, if it 
     * is not provided, then the qid is used to construct
     * the url. */
    url: PropTypes.string,

    /** The query id of the character to be rendered, will
     * be omitted if url is present and not null. */
    qid: PropTypes.number,

    // new alwaysDisplay prop.
    alwaysDisplay: PropTypes.bool,
};
CharDisplay.defaultProps = {
    alwaysDisplay: false,
};