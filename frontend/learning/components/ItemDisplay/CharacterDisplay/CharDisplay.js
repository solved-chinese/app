import React from 'react';
import 'core-js/stable';
import 'regenerator-runtime/runtime';
import PropTypes from 'prop-types';
import styled from 'styled-components';

import CharDefinition from './CharDefinition.js';

import RelatedItems from '@learning.components/ItemDisplay/RelatedItems';
import ItemPhonetic from '@learning.components/ItemDisplay/ItemPhonetic';
import BreakdownView from '@learning.components/ItemDisplay/BreakdownView';
import LoadingView from '@learning.components/ItemDisplay/LoadingView';

import useLoadChar from '@learning.hooks/useLoadChar';

import '@learning.styles/ItemDisplay.css';

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

    const character = props.character == null?
        useLoadChar(
        props.url == null ?
            `/content/character/${props.qid}` : props.url
        ) : props.character;

    const renderCharacter = () => {
        const definitions = character.definitions.map( v => 
            v.definition
        );
        return (
            <>
                <Row>
                    <ItemPhonetic pinyin={character.pinyin}
                        audioURL={character.audioUrl}
                        item={character.chinese}/>
                    <CharDefinition 
                        definitions={ definitions }
                    />
                </Row>
                <RelatedItems 
                    items={character.relatedWords}
                    item={character.chinese}
                    itemType='word' />
                <BreakdownView type='radical'
                    componentURL={character.radicals}
                    memoryAid={character.memoryAid}
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
    /** The character object to be rendered, if not provides,
     *  url will be used to construct the object.
     */
    character: PropTypes.object,

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