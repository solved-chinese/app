import React from 'react';
import styled from 'styled-components';

import CharDefinition from './CharDefinition';

import RelatedItems from '@learning.components/ItemDisplay/RelatedItems';
import ItemPhonetic from '@learning.components/ItemDisplay/ItemPhonetic';
import BreakdownView from '@learning.components/ItemDisplay/BreakdownView';
import LoadingView from '@learning.components/ItemDisplay/LoadingView';
import useLoadChar from '@learning.hooks/useLoadChar';

import {Character} from '@interfaces/CoreItem';

import '@learning.styles/ItemDisplay.css';

const Row = styled.div`
    display: flex;
    justify-content: center;
    align-items: center;
    @media only screen and (max-width: 480px) {
        flex-direction: column;
    }
`;

type Props = {
    /**
     *  The character object to be rendered, if not provided,
     *  url will be used to fetch the object.
     */
    character?: Character,

    /**
     * The URL of the character to be rendered, if it
     * is not provided, then the qid is used to construct
     * the url.
     */
    url?: string,

    /**
     * The query id of the character to be rendered, will
     * be omitted if url is present and not null.
     */
    qid?: number,

    /**
     * Whether the breakdown view is always expanded.
     */
    autoExpandBreakdown?: boolean,
}

/**
 * The main function that renders a character view.
 */
const CharDisplay = (props: Props): JSX.Element => {

    const character = props.character == null?
        useLoadChar(
            props.url == null ?
                `/content/character/${props.qid}` : props.url
        ) : props.character;

    const renderCharacter = (character: Character) => {
        const definitions = character.definitions.map( v => 
            v.definition
        );
        const autoExpandBreakdown = props.autoExpandBreakdown ?? true;
        return (
            <>
                <Row>
                    <ItemPhonetic
                        pinyin={character.pinyin}
                        audioURL={character.audioUrl}
                        item={character.chinese}
                        useStroke={true}
                    />
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
                    alwaysDisplay={autoExpandBreakdown}
                />
            </>
        );
    };

    if (character === null) {
        return <LoadingView />;
    } else {
        return renderCharacter(character);
    }
};

export default CharDisplay;
