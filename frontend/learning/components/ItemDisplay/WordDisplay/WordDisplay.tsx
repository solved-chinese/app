import React from 'react';
import styled from 'styled-components';

import WordDefinition from './WordDefinition';
import ExampleSentences from './ExampleSentences';

import BreakdownView from '@learning.components/ItemDisplay/BreakdownView';
import LoadingView from '@learning.components/ItemDisplay/LoadingView';
import useLoadWord from '@learning.hooks/useLoadWord';

import { Word } from '@interfaces/CoreItem';

//Top and Bottom Containers
const ContainerTop = styled.div`
    display: flex;
    justify-content: center;
    align-items: center;
    @media only screen and (max-width: 480px) {
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

type Props = {
    /**
     * The word object to be rendered, if not provided,
     * url will be used to construct the object.
     */
    word?: Word,

    /**
     * The URL of the word to be rendered, if it
     * is not provided, then the qid is used to construct
     * the url.
     */
    url?: string,

    /**
     * The query id of the word to be rendered, will
     * be omitted if url is present and not null.
     */
    qid?: number,

    /* Determine whether the breakdown view is always expanded. */
    autoExpandBreakdown?: boolean,
}

/**
 * The main function that renders a word view.
 */
const WordDisplay = (props: Props): JSX.Element => {

    const word: Word | null = props.word == null ?
        useLoadWord(props.url == null ?
            `/content/word/${props.qid}` : props.url
        ) : props.word;

    const renderBreakdown = (word: Word): JSX.Element => {
        // if it is single-character word, the characters field will be a list of
        // a single serialized character, render that character's breakdown view
        if (word.characters.length === 1) {
            const radicals = word.characters[0].split(';');
            return (
                <BreakdownView
                    type='radical'
                    alwaysDisplay={props.autoExpandBreakdown ?? true}
                    componentURL={radicals}
                    memoryAid={word.memoryAid}
                />
            );
        } else {
            return (
                <BreakdownView
                    type='word'
                    alwaysDisplay={props.autoExpandBreakdown ?? true}
                    componentURL={word.characters}
                    memoryAid={word.memoryAid}
                />
            );
        }
    };

    const renderWord = (word: Word): JSX.Element => {
        const chinese = word.chinese;
        const pinyin = word.pinyin;
        const definitions = word.definitions;
        const audioURL = word.audioUrl;
        
        return (
            <>
                {/* Top: Word Definition*/}
                <ContainerTop>
                    <WordDefinition 
                        audioURL= {audioURL}
                        chinese={chinese}
                        pinyin={pinyin}
                        definitions={definitions}
                    />
                </ContainerTop>

                { renderBreakdown(word) }
                <br/>

                <ExampleSentenceHeading>
                    Example Sentences
                </ExampleSentenceHeading>
                
                <ContainerBottom>
                    {word.sentences.map((sen) => {
                        return (
                            <ExampleSentences
                                key={sen.chineseHighlight}
                                word={word}
                                pinyin={sen.pinyinHighlight}
                                audioURL={sen.audioUrl}
                                chinese={sen.chineseHighlight}
                                translation={sen.translationHighlight}
                            />
                        );
                    })}
                </ContainerBottom>
            </>
        );
    };

    if (word === null) {
        return <LoadingView />;
    } else {
        return renderWord(word);
    }
};

export default WordDisplay;
