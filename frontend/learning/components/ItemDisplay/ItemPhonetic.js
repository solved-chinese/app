import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import '@learning.styles/ItemDisplay.css';
import StrokeGif from '@learning.components/ItemDisplay/StrokeGif';

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

export const SpeakButton = styled.img`
    position: relative;
    margin-left: 3px;
    font-weight: 200; //changed from 200
    cursor: pointer;
    transform: scale(0.6);    
`;

const WordContainer = styled.h1`
    font-size: 3.75em;
    font-weight: 200;
    text-align: center;
`;

/**
 * Renders the Chinese, phonetic(pinyin), and an audio button.
 * @param {String} props.pinyin
 * @param {String} props.audioURL
 * @param {String} props.item
 * @param {Boolean} props.useStroke
 * @return {JSX.Element}
 */
export default function ItemPhonetic(props) {

    const audio = new Audio(props.audioURL);
    // Add slashes at the beginning and the end
    const pinyin = `/${props.pinyin}/`;

    const renderWord = () => props.useStroke ?
        <StrokeGif item={props.item}/> :
        <WordContainer className='use-chinese'>
            { props.item }
        </WordContainer>;

    return (
        <Container>
            <Phonetic className='use-chinese'>
                { pinyin }
                <SpeakButton
                    src="/static/images/small-icons/pronounce.svg"
                    // className='fas fa-volume' // changed to svg
                    onClick={() => audio.play()}
                />
            </Phonetic>
            { renderWord() }
        </Container>
    );
}

ItemPhonetic.defaultProps = {
    useStroke: false
};

ItemPhonetic.propTypes = {
    /** An array of possible pronunciation. */
    pinyin: PropTypes.string,
    /** The URL of the corresponding audio file. */
    audioURL: PropTypes.string.isRequired,
    /** The character to be displayed. */
    item: PropTypes.string.isRequired,
    /** Whether to enable stroke order. */
    useStroke: PropTypes.bool
};
