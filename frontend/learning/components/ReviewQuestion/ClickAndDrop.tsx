import React, { useState, useEffect } from 'react';
import styled from 'styled-components';

import {CNDQuestionContent, AnswerVerificationResponse, ReviewQuestionAnswer} from '@interfaces/ReviewQuestion';

import '@learning.styles/ReviewQuestion.css';

import AnswerResponse from './AnswerResponse';

// buttons
const AnswerButton = styled.button`
    width: 50px;
    height: 50px;
    margin-left: auto;
    margin-right: auto;
    border-radius: 10px;
    border: none;
    font-size: 1.5rem;
    text-align: center;
    color: black;
    outline: none;
    box-shadow:none;
`;

const ChoiceButton = styled.button`
    width: 50px;
    height: 50px;
    margin-left: auto;
    margin-right: auto;
    border-radius: 10px;
    background-color: white;
    border-color: gray;
    font-size: 1.5rem;
    text-align: center;
    color: gray;
    outline: none;
    box-shadow: none;
`;

//Prompts
const Description = styled.h1`
    font-size: 1.6em;
    margin-bottom: 40px;
    text-align: center;
    color: var(--primary-text);
`;

const Question = styled.h2`
    font-size: 1.5em;
    margin-bottom: 30px;
    text-align: left;
    font-weight: 900;
    color: var(--primary-text);
`;

//Containers
const ChoicesContainer = styled.div`
    display: flex;
    text-align: center;
    flex-direction: row;
    margin-right: auto;
    margin-left: auto;
    height: 20%;
    width: 50%;
    padding-bottom: 1.5em;
`;

const AnswerContainer = styled.div`
    display: flex;
    text-align:center;
    background-color: white;
    flex-direction: row;
    width: 20%;
    margin-left: auto;
    margin-right: auto;
    padding-bottom: 1.5em;
    height: 20%;
`;

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
    content: CNDQuestionContent,
    submitAnswer: (answer: ReviewQuestionAnswer) => Promise<[AnswerVerificationResponse, NextActionCallback]>,
}

/**
 * Render a CND component.
 */
const ClickAndDrop = (props: Props): JSX.Element => {
    const [selected, setSelected] = useState<(string|null)[]>(
        Array<string|null>(props.content.answerLength).fill(null)
    );
    const [choices, setChoices] = useState<(string|null)[]>([...props.content.choices]);
    const [submitted, setSubmitted] = useState<boolean>(false);
    const [isAnswerCorrect, setIsAnswerCorrect] = useState<boolean|undefined>(undefined);
    const [correctAnswer, setCorrectAnswer] = useState<string>('');
    const [nextActionCallback, setNextActionCallback] = useState<{ fn: NextActionCallback }>({fn: () => {
        // Do nothing
    }});

    useEffect(() => {
        setSelected(Array(props.content.answerLength).fill(null));
        setChoices([...props.content.choices]);
        setSubmitted(false);
        setCorrectAnswer('');
        setIsAnswerCorrect(undefined);
    }, [props]);

    useEffect(() => {
        if (selected.every(value => value != null))
            onSubmit();
    }, [selected]);

    useEffect(() => {
        if (isAnswerCorrect) {
            const timer = setTimeout(nextActionCallback.fn, 500);
            return () => clearTimeout(timer);
        }
    }, [isAnswerCorrect]);

    const onSubmit = () => {
        if (submitted)
            return;
        props.submitAnswer(selected as string[]).then(([response, callbackFn]) => {
            setSubmitted(true);
            setCorrectAnswer((response.answer as string[]).join(''));
            setNextActionCallback({fn: callbackFn});
            setIsAnswerCorrect(response.isCorrect);
        }).catch( msg => {
            console.log(msg);
        });
    };

    let buttonClassName = '';
    if (isAnswerCorrect != null) {
        buttonClassName += isAnswerCorrect ? ' cndCorrect' : ' cndIncorrect';
    }

    const handleChoiceClick = (choiceIndex: number) => {
        if (choices[choiceIndex] === null || submitted){
            return; // meaningless click on blank
        }
        const selectedIndex = selected.findIndex(value => value===null);
        if (selectedIndex === -1){
            return; // select full
        }
        // make copy
        const newSelected = selected.slice();
        const newChoices = choices.slice();
        // move clicked choice to selected
        newSelected[selectedIndex] = newChoices[choiceIndex];
        newChoices[choiceIndex] = null;
        setSelected(newSelected);
        setChoices(newChoices);
    };

    const handleSelectedClick = (selectedIndex: number) => {
        if (selected[selectedIndex] === null || submitted){
            return; // meaningless click on blank
        }
        if (selectedIndex === -1){
            return; //select full
        }
        // make copy
        const newSelected = selected.slice();
        const newChoices = choices.slice();
        // move selected choice to choices
        const choiceIndex = choices.findIndex(value => value===null);
        newChoices[choiceIndex] = newSelected[selectedIndex];
        newSelected[selectedIndex] = null;
        setSelected(newSelected);
        setChoices(newChoices);
    };

    const showSelected = (() => {
        return selected.map((value, i) =>
            <AnswerButton
                className={buttonClassName}
                key={i}
                onClick={() => {
                    handleSelectedClick(i);
                }}
            >
                {value === null? ' ' : value}
            </AnswerButton>
        );
    })();

    const showChoices = (() => {
        return choices.map((value, i) =>
            <ChoiceButton
                key={i}
                style={{width: '50px', height: '50px'}}
                onClick={() => {
                    handleChoiceClick(i);
                }}
            >
                {value === null? ' ' : value}
            </ChoiceButton>
        );
    })();


    return (
        <div className='question-content'>
            <div style={{width: '100%'}}>
                <Question className='use-chinese'>
                    {props.content.question}
                </Question>
                <Description>
                    {props.content.description}
                </Description>
                <Description>
                    {props.content.title}
                </Description>
                <AnswerContainer>
                    {showSelected}
                </AnswerContainer>
                <ChoicesContainer>
                    {showChoices}
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
                {submitted ?
                    <AnswerResponse isCorrect={isAnswerCorrect!} correctAnswer={correctAnswer}/> : ''}
            </div>
        </div>
    );
};

export default ClickAndDrop;
