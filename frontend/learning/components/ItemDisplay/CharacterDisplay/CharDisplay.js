import React from 'react';
import 'core-js/stable';
import 'regenerator-runtime/runtime';
import PropTypes from 'prop-types';
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

/**
 * The main function that renders a character view.
 * @param {?Character} props.character The character object to be rendered,
 * if not provided, the url param will be used to fetch the object.
 * @param {?string} props.url The URL of the character to be rendered, if
 * not provided, the qid is used to construct the url.
 * @param {?number} props.qid The query id of the character to be rendered,
 * will be omitted if either character or url is not null.
 * @param {?boolean} props.autoExpandBreakdown Whether the breakdown view is
 * always expanded.
 * @returns {JSX.Element}
 */
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
                    alwaysDisplay={props.autoExpandBreakdown}
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
    /**
     *  The character object to be rendered, if not provided,
     *  url will be used to fetch the object.
     */
    character: PropTypes.object,

    /**
     * The URL of the character to be rendered, if it
     * is not provided, then the qid is used to construct
     * the url.
     */
    url: PropTypes.string,

    /**
     * The query id of the character to be rendered, will
     * be omitted if url is present and not null.
     */
    qid: PropTypes.number,

    /**
     * Whether the breakdown view is always expanded.
     */
    autoExpandBreakdown: PropTypes.bool,
};

CharDisplay.defaultProps = {
    autoExpandBreakdown: true,
};