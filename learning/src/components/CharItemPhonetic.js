import React from 'react';
import { render } from 'react-dom';
import PropTypes from 'prop-types';
import styled from 'styled-components';

const Container = styled.div`
    display: inline-block;
    flex-wrap: wrap;
    width: auto;
`;

const Phonetic = styled.span`
    text-align: center;
    font-size: 1.5em;
    font-weight: 200;
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
 * 
 */
export default class CharItemPhonetic extends React.Component {

    static propTypes = {
        /** An array of possible pronunciation. */
        pinyin: PropTypes.arrayOf(
            PropTypes.string
        ).isRequired,
        /** The URL of the corresponding audio file. */
        audioURL: PropTypes.string.isRequired,
        /** The character to be displayed.  */
        character: PropTypes.string.isRequired
    }

    constructor(props) {
        super(props);
        this.audio = new Audio(props.audioURL);

        // Add slashes in the beginning and the end of each
        // pronunciation and joined with 'or'
        this.pinyin = props.pinyin.map(v => `/${v}/`).join(' or ');
    }

    play() {
        this.audio.play();
    }

    render() {
        return (
            <Container>
                <Phonetic className='use-serifs'> 
                    { this.pinyin }
                    <SpeakButton className='fas fa-volume'
                        onClick= {this.play} ></SpeakButton>
                </Phonetic>
                <WordContainer className='use-serifs'>
                    { this.props.character }
                </WordContainer>
            </Container>
        );
    }
}