import React from 'react';
import 'core-js/stable';
import 'regenerator-runtime/runtime';
import PropTypes from 'prop-types';
import styled from 'styled-components';

import WordDefinition from './WordDefinition';
import ExampleSentences from './ExampleSentences';
import BreakdownView from './BreakdownView';

import LoadingView from './LoadingView.js';

//Top and Bottom Containters
const ContainerTop = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  @media (max-width: 768px) {
      flex-direction: column;
    }
`;

const ContainerBottom = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  @media (max-width: 768px) {
    flex-direction: column;
  }
`;

export default class WordDisplay extends React.Component {
    
    static propTypes = {
        qid: PropTypes.number
    }

    constructor(props) {
        super(props);
        this.state ={
            word: null,
            loading: true
        };
    }

    componentDidMount() {
        this.loadData();
    }

    async loadData() {
        const response = await fetch(`/content/word/${this.props.qid}`);
        if (!response.ok) {
            setTimeout(() => {
                this.loadData();
            }, 5);
            throw new Error(`An ${response.status} error has occured,
                retrying in 5 seconds.`);
        }

        // parse the response object into json
        const data = await response.json();
        // use the json object to update component states
        this.setState({ word: data, loading: false});
    }

    showLoadingView() {
        return <LoadingView />;
    }


    showContent() {
        const word = this.state.word;
        const chinese = word.chinese;
        const pinyin = word.pinyin;
        const definitions = word.definitions;
        const sentence1 =word.sentences[0];
        const sentence2 =word.sentences[1];
        
        return (
            <>
                {/* Top: Word Definition*/}
                <ContainerTop>
                    <WordDefinition 
                        audioURL= ''
                        chinese={chinese}
                        pinyin={pinyin}
                        definitions={definitions}
                        // [{definition: 'student', part_of_speech: 'n.'}, 
                            // {definition:"manymnayahsujfiejfiej", part_of_speech:'adj.'}]
                    />
                </ContainerTop>

                {/* Bottom: Example Sentences */}
                <p style={{textAlign: 'center', marginTop: '10px', fontSize: '13px'}}>Example Sentences:</p>
                <ContainerBottom>
                    <ExampleSentences 
                        word={word}
                        pinyin={sentence1.pinyin}
                        chinese={sentence1.chinese} 
                        translation={sentence1.translation}
                    />
                    <ExampleSentences 
                        word={word}
                        pinyin={sentence2.pinyin}
                        chinese={sentence2.chinese} 
                        translation={sentence2.translation}
                    />
                </ContainerBottom>
        
                {/* Show Breakdown toggle. Borrowed from Michael*/}
                {/* <BreakdownView /> */}

            </>
        );
    }

    render() {
        // Display a loading page while `this.state.loading == true`.
        return this.state.loading ? 
            this.showLoadingView() : this.showContent();
    }
}