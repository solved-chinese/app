import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';

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

    constructor(props) {
        super(props);
        this.audio = new Audio(props.audioURL);
        // Add slashes at the beginning and the end
        this.pinyin = `/${this.props.pinyin}/`;
        
    }


    play() {
        this.audio.play();
    }

    render() {
        return (
            <Container>
                <Phonetic className='use-chinese'> 
                    { this.pinyin }
                    <SpeakButton className='fas fa-volume'
                        onClick= {() => this.play()} ></SpeakButton>
                </Phonetic>
                <WordContainer className='use-chinese'>
                    { this.props.item }
                </WordContainer>
            </Container>
        );
    }
}