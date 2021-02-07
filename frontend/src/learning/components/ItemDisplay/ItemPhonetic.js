import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';
// npm install hanzi-writer, Hanzi object created on line 56
import HanziWriter from 'hanzi-writer';
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
        this.item = `${this.props.item}`;

        // Is it possible to contruct writer component in constructor?

        // this.writer1 = HanziWriter.create('div-1', '我', {
        //     width: 100,
        //     height: 100,
        //     padding: 5,
        //     showOutline: true
        // });

        
    }
    
    // Temporary half-solution
    // Because ItemPhonetic is used by WordBreakdown and PopUp,
    // componentDidMount will mount them at once (all stacks on one spot)? 
    // Maybe mount and unmount every call?
    //
    componentDidMount (){
        var writer = HanziWriter.create('div-writer', this.item, {
            width: 100,
            height: 100,
            padding: 5,
            showOutline: true
        });
        document.getElementById('div-writer').addEventListener('click', function() {
            writer.animateCharacter();
        });
    }

    play() {
        this.audio.play();
    }

    render() {
        return (
            <Container>
                <Phonetic className='use-chinese'> 
                    { this.pinyin }
                    <SpeakButton 
                        className='fas fa-volume'
                        onClick={() => this.play()} 
                    ></SpeakButton>
                </Phonetic>
                <WordContainer className='use-chinese'>
                    {/* { this.item } */}
                    {/* Writer Div here */}
                    <div id='div-writer' style={{cursor: 'grab'}}></div> 
                    
                </WordContainer>
            </Container>
        );
    }
}