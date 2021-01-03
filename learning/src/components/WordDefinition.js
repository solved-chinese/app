import React, { Component } from 'react';
import { render } from 'react-dom';
import PropTypes from 'prop-types';
import styled from 'styled-components';

const CardContainer =styled.div`
    display: flex;
    flex-wrap: wrap;
    width: auto;
    padding: 2em auto 1em auto;
    justify-content: center;
`;

const Container = styled.span`
    display: inline-block;
    flex-wrap: wrap;
    width: auto;
    padding: 0 3em 0 2em;
`;

const SpeakButton = styled.i`
    font-weight: 200;
    cursor: poiter;
`;

const WordContainer = styled.h1`
    font-size: 3.5em;
    fontweight: 200;
`;

const TableContainer = styled.table`
    margin-top: 2em;
    border-left: 2px solid var(--teritary-text);
    border-collapse: collapse;
    font-size: 1em;
`;

const CellLeft = styled.td`
    padding: 0 0.6em 0 0.1em;
    text-align: right;
`;

const ListTitle = styled.i`
    font-size: 0.7em;
    font-style: normal;
    color: var(--teritary-text);
    line-height: 1em;
    padding-left: 1em;
`;

class WordPinyinSound extends React.Component {
    
    static propTypes = {
        chinese: PropTypes.string.isRequired,
        audioURL: PropTypes.string.isRequired,
        pinyin: PropTypes.string.isRequired
    }

    constructor(props) {
        super(props);
        this.audio = new Audio(props.audioURL);
    }

    render() {
        return (
            <Container>
                <WordContainer className='use-serif'>
                    <ruby>
                        {this.props.chinese}
                        <rp>(</rp>
                        <rt>{this.props.pinyin}</rt>
                        <rp>)</rp>
                    </ruby>
                </WordContainer>
                <SpeakButton 
                    className='fas-fa-volume' 
                    onClick={()=>this.audio.play()}></SpeakButton>
            </Container>
        );
    }
}

class Definitions extends React.Component {
    render() {
        const definitions = this.props.definitions.map(d => {
            return (
                <tr key={d.part_of_speech}>
                    <CellLeft>{d.part_of_speech}</CellLeft>
                    <td>{d.definition}</td>
                </tr>
            );
        });

        return (
            <TableContainer>
                <ListTitle>Definition</ListTitle>
                {definitions}
            </TableContainer>
        );
    }
}
export default class WordDefinition extends React.Component {

    static propTypes = {
        chinese: PropTypes.string.isRequired,
        audioURL: PropTypes.string.isRequired,
        pinyin: PropTypes.string.isRequired,
        definitions: PropTypes.arrayOf(
            PropTypes.objectOf(
                PropTypes.string
            )
        ),
    } 

    render() {
        return (
            <CardContainer>
                <WordPinyinSound
                    chinese={this.props.chinese} 
                    pinyin={this.props.pinyin}
                    audioURL={this.props.audioURL}
                />
                <Definitions
                    definitions={this.props.definitions}
                />
            </CardContainer>
        );
    }
}