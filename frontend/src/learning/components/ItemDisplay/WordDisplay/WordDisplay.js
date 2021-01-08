import React from 'react';
import 'core-js/stable';
import 'regenerator-runtime/runtime';
import PropTypes from 'prop-types';
import styled from 'styled-components';

import WordDefinition from './WordDefinition';
import ExampleSentences from './ExampleSentences';

import BreakdownView from '@learning.components/ItemDisplay/BreakdownView';
import LoadingView from '@learning.components/ItemDisplay/LoadingView.js';

import useLoadWord from '@learning.hooks/useLoadWord.js';

//Top and Bottom Containters
const ContainerTop = styled.div`
    display: flex;
    justify-content: center;
    align-items: center;
    @media only screen and (max-width: 480) {
        flex-direction: column;
    }
`;

const ContainerBottom = styled.div`
    display: flex;
    justify-content: center;
    align-items: center;
    @media only screen and (max-width: 768px) {
        flex-direction: column;
    }
`;

const ExampleSentenceHeading = styled.h2`
    color: var(--teritary-text);
    margin-top: 10px;
    font-size: 0.9em;
    font-weight: 400;
    text-align: center;
`;

/** The main function that renders a word view. */
export default function WordDisplay(props) {

    const word = useLoadWord(`/content/word/${props.qid}`);

    const renderWord = (word) => {
        const chinese = word.chinese;
        const pinyin = word.pinyin;
        const definitions = word.definitions;
        
        return (
            <>
                {/* Top: Word Definition*/}
                <ContainerTop>
                    <WordDefinition 
                        audioURL= ''
                        chinese={chinese}
                        pinyin={pinyin}
                        definitions={definitions}
                    />
                </ContainerTop>

                {/* Bottom: Example Sentences */}
                <ExampleSentenceHeading>
                    Example Sentences
                </ExampleSentenceHeading>
                <ContainerBottom>
                    {word.sentences.map((sen, i) => {
                        return (
                            <ExampleSentences
                                key={word}
                                word={word}
                                pinyin={sen.pinyin}
                                chinese={sen.chinese} 
                                translation={sen.translation}
                            />
                        );
                    })}
                </ContainerBottom>
        
                {/* Show Breakdown toggle. Borrowed from Michael*/}
                <BreakdownView 
                    type='word'
                    componentURL={word.characters}
                    memoryAid={word.memory_aid}
                    qid={props.qid} //Question Mark
                />
            </>
        );
    };

    if (word === null) {
        return <LoadingView />;
    } else {
        return renderWord(word);
    }
}

WordDisplay.propTypes = {
    qid: PropTypes.number.isRequired
};