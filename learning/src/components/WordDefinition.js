import React, { Component } from 'react';
import { render } from 'react-dom';

function SoundButton(props) {
    return (
        <div>
            <i 
                className="fas fa-volume"
                id="sound-button"
                onClick={() => document.getElementById('audio').play()}
            ></i>
            <audio id="audio">
                <source src={props.src} type="audio/mpeg"></source>
            </audio>
        </div>
    );
}

function WordPinyin(props) {
    return (
        <ruby>
            {props.word}
            <rp>(</rp>
            <rt>{props.pinyin}</rt>
            <rp>)</rp>
        </ruby>
    );
}

class Definitions extends React.Component {
    render() {
        const definitions = this.props.definitions.map(d => {
            return (
                <tr key={d.part_of_speech}>
                    <td>{d.part_of_speech}</td>
                    <td>{d.definition}</td>
                </tr>
                // <li key ={d.part_of_speech}>
                //     {d.part_of_speech + d.definition}
                // </li>
            );
        });

        return (
            <table>
                {definitions}
            </table>
        );
    }
}
class WordDefinition extends React.Component {
    render() {
        const cn = this.props.word;
        const py = this.props.pinyin;
        const audiosrc = this.props.audiosrc;
        const arr = this.props.definitions;

        return (
            <div className="worddefinition">
                <div className="wordpinyin">
                    <WordPinyin 
                        word={cn} 
                        pinyin={py}
                    />
                    <SoundButton src={audiosrc}/>
                </div>
                <div className="definition">
                    <Definitions
                        definitions={arr}
                    />
                </div>
            </div>
        );
    }
}

export default WordDefinition;