import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';

import '@learning.styles/ItemDisplay.css';

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
 */
export default class ItemPhonetic extends React.Component {

    static propTypes = {
        /** An array of possible pronunciation. */
        pinyin: PropTypes.string,
        /** The URL of the corresponding audio file. */
        audioURL: PropTypes.string.isRequired,
        /** The character to be displayed.  */
        item: PropTypes.string.isRequired
    }

    render() {
        this.audio = new Audio(this.props.audioURL);
        // Add slashes at the beginning and the end
        this.pinyin = `/${this.props.pinyin}/`;
        return (
            <Container>
                <Phonetic className='use-chinese'> 
                    { this.pinyin }
                    <SpeakButton
                        src="/static/images/small-icons/pronounce.svg"
                        // className='fas fa-volume' // changed to svg
                        onClick={() => this.audio.play()}
                    />

                </Phonetic>
                <WordContainer className='use-chinese'>
                    { this.props.item }
                </WordContainer>
            </Container>
        );
    }
}