import React, {useState, useEffect, CSSProperties} from 'react';
import * as Sentry from '@sentry/react';
import styled from 'styled-components';

import {
    AnswerVerificationResponse,
    MCAnswer,
    MCQuestionContent,
    ReviewQuestionAnswer
} from '@interfaces/ReviewQuestion';
import AnswerResponse from './AnswerResponse';
import { getTextAudio } from '@utils/utils';


import '@learning.styles/ReviewQuestion.css';

export const SpeakButton1 = styled.img`
    position: relative;
    margin-left: 3px;
    margin-bottom: 5px;
    font-weight: 200; 
    cursor: pointer;
    transform: scale(0.9);    
`;
export const SpeakButton2 = styled.img`
    position: relative;
    margin-left: 11px;
    margin-bottom: 5px;
    font-weight: 100; 
    cursor: pointer;
    transform: scale(0.7);    
`;

const Context = styled.h1`
    font-size: 1.6em;
    margin-bottom: 30px;
    color: var(--primary-text);
`;

const Question = styled.h2`
    font-size: 2em;
    margin-bottom: 30px;
    margin-left: 0.7em;
    font-weight: 600;
`;

const ChoicesContainer = styled.div`
    display: flex;
    flex-direction: row;
    padding: 0 0 30px 20px;
    margin: 120px auto;
    flex-wrap: wrap;

`;

// overriding the buttons within ChoicesContainer
const newButton: CSSProperties = {
    flexDirection: 'column',
    textAlign: 'left',
    padding: '5px 15px 5px',
    margin: '10px 10px 0 0',
    minHeight: '75px',
    width: '207px',
    wordWrap: 'break-word',
};

const SubmitContainer = styled.div`
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    justify-content: space-between;
    font-size: 14px;
    width: 100%;
`;

type NextActionCallback = () => void;

type Props = {
    content: MCQuestionContent,
    submitAnswer: (answer: ReviewQuestionAnswer) => Promise<[AnswerVerificationResponse, NextActionCallback]>,
}

/**
 * Render a multiple choice (MC) component.
 */
const MultipleChoice = (props: Props): JSX.Element => {

    const [selectedAnswer, setSelectedAnswer] = useState<MCAnswer | undefined>(undefined);
    const [correctAnswer, setCorrectAnswer] = useState<MCAnswer | undefined>(undefined);
    const [submitted, setSubmitted] = useState<boolean>(false);
    const [isAnswerCorrect, setIsAnswerCorrect] = useState<boolean | undefined>(undefined);
    const [nextActionCallback, setNextActionCallback] = useState<{ fn: NextActionCallback }>({fn: () => {
        // Do nothing
    }});

    useEffect( () => {
        setSelectedAnswer(undefined);
        setCorrectAnswer(undefined);
        setSubmitted(false);
        setIsAnswerCorrect(undefined);
    }, [props]);

    useEffect(() => {
        if (selectedAnswer && !submitted)
            onSubmit(selectedAnswer);
    }, [selectedAnswer]);

    useEffect(() => {
        if (submitted && isAnswerCorrect) {
            const timer = setTimeout(nextActionCallback.fn, 500);
            return () => clearTimeout(timer);
        }
    }, [isAnswerCorrect]);

    const onSubmit = (answer: MCAnswer) => {
        props.submitAnswer(answer).then(([response, callback]) => {
            setCorrectAnswer(response.answer as MCAnswer);
            setSubmitted(true);
            setNextActionCallback({fn: callback});
            setIsAnswerCorrect(response.isCorrect);
        }).catch( error => {
            Sentry.captureException(error);
        });
    };
    // change: remove use-serif   
    const getChoiceClassName = (value: string) => {
        let name = 'choice-button';
        if (value == selectedAnswer) {
            if (correctAnswer != null) {
                name += value == correctAnswer ? ' correct' : ' incorrect';
            } else {
                name += ' active';
            }
        } else if (value == correctAnswer) {
            name += ' correct';
        }
        return name;
    };

    const choiceOnClickCallback = (text: string) => {
        if (!submitted) {
            if (selectedAnswer !== text) {
                setSelectedAnswer(text);
            } else {
                setSelectedAnswer(undefined);
            }
        }
    };

    const choices = (() => {
        return props.content.choices.map( (v, i) => {
            const [text, audio] = getTextAudio(v);
            return (
                <div key={i}>
                    <button
                        key={i} // change text to i
                        className={getChoiceClassName(text)}
                        style={newButton}
                        onClick={() => choiceOnClickCallback(text)}
                    >
                        {text}
                    </button>
                    {audio? <SpeakButton1
                        src="/static/images/small-icons/pronounce.svg"
                        onClick={() => new Audio(audio).play()}/> : null}
                </div>
            );
        }
        );
    })();

    const context = (() => {
        if ('context' in props.content) {
            const result = getTextAudio(props.content.context);
            let text = result[0];
            const audio = result[1];
            // add highlight of sentences similar to that in word display
            text = text.replace(
                new RegExp('<(.*?)>', 'g'),
                '<span style=\'color: #00838F\'>$1</span>'
            );
            return (
                <Context className='use-chinese'>
                    <span dangerouslySetInnerHTML={{__html: text}}/>
                    {audio ? <SpeakButton1
                        src="/static/images/small-icons/example-sentence.svg"
                        onClick={() => new Audio(audio).play()}/> : null}
                </Context>
            );
        }
        return null;
    })();

    return (
        <div className='question-content'>
            <div style={{width: '100%'}}>
                {context}
                <Question>
                    {(() => {
                        const [text, audio] = getTextAudio(props.content.question);
                        return (<>
                            {text}
                            {audio? <SpeakButton2
                                src="/static/images/small-icons/pronounce.svg"
                                onClick={() => new Audio(audio).play()}/> : null}
                        </>);
                    })()}
                </Question>
                <ChoicesContainer>
                    {choices}
                </ChoicesContainer>
                <SubmitContainer>
                    <button
                        className="choice-button"
                        hidden={!submitted || (submitted && isAnswerCorrect)}
                        onClick={nextActionCallback.fn}
                    >
                        Next
                    </button>
                </SubmitContainer>
                {submitted? <AnswerResponse
                    isCorrect={isAnswerCorrect!}
                    correctAnswer={correctAnswer!}
                /> : ''}
            </div>
        </div>
    );
};

export default MultipleChoice;
