// This is the new ItemGif 
//      a motified version of ItemPhonetic
//      used only in wordDisplay

import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import '@learning.styles/ItemDisplay.css';

import StrokeGif from './StrokeGif.js';

const Container = styled.div`
    display: inline-block;
    width: auto;
`;

const Phonetic = styled.span`
    text-align: center;
    font-size: 1.5em;
    font-weight: 200;
    white-space: nowrap;
`;

const SpeakButton = styled.i`
    position: relative;
    margin-left: 5px;
    font-weight: 200;
    cursor: pointer;
`;

/**
 * Renders the Chinese, phonetic(pinyin), and an audio button.
 */
export default function ItemPhonetic(props) {

    const audio = new Audio(props.audioURL);
    // Add slashes at the beginning and the end
    const pinyin = `/${props.pinyin}/`;

    return (
        <Container>
            <Phonetic className='use-chinese'>
                { pinyin }
                <SpeakButton
                    className='fas fa-volume'
                    onClick={ audio.play }
                />
            </Phonetic>
            
            {/* new StrokeGif */}
            <StrokeGif item={props.item}/>

        </Container>
    );
}

ItemPhonetic.propTypes = {
    /** An array of possible pronunciation. */
    pinyin: PropTypes.string,
    /** The URL of the corresponding audio file. */
    audioURL: PropTypes.string.isRequired,
    /** The character to be displayed.  */
    item: PropTypes.string.isRequired
};

// http://127.0.0.1:8000/content/display/word/1