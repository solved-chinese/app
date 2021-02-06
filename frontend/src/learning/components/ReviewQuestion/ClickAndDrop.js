import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import PropTypes from 'prop-types';

import { CNDQuestionContent } from '@interfaces/ReviewQuestion';

import submitAnswer from '@learning.services/submitAnswer';

import '@learning.styles/ReviewQuestion.css';

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
    font-weight: 400;
    color: var(--primary-text);
`;

const ChoicesContainer = styled.div`
    display: flex;
    text-align: center;
    flex-direction: row;
    margin-right: 50px;
    height: 20%;
`;

const AnswerContainer = styled.div`
    display: flex;
    text-align:center;
    background-color: gray;
    flex-direction: row;
    margin-right: 50px;
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

/**
 * Render a CND component.
 * @param {Object} props 
 * @param {CNDQuestionContent} props.content
 * @param {Function} props.submitAnswer
 * @param {Function} props.onActionNext
 *
 * @returns {React.Component}
 */
export default function ClickAndDrop(props) {
    const [selected, setSelected] = useState(Array(props.content.answerLength).fill(null));
    const [choices, setChoices] = useState([...props.content.choices]);
    const [submitted, setSubmitted] = useState(false);

    useEffect(() => {
        setSelected(Array(props.content.answerLength).fill(null));
        setChoices([...props.content.choices]);
        setSubmitted(false);
    }, [props])

    const onSubmit = () => {
        props.submitAnswer(selected).then(response => {
            setSubmitted(true);
            setCorrectAnswer(response.answer);
            setChoices(choices.slice().fill(' '))
            alert("is_correct: " + response.isCorrect);
        }).catch( msg => {
            console.log(msg);
        });
    };

    const setCorrectAnswer = (correctAnswer) => {
        setSelected(correctAnswer);
    };

    const handleChoiceClick = (choiceIndex) => {
        if (choices[choiceIndex] === null)
            return; // meaningless click on blank
        const selectedIndex = selected.findIndex(value => value===null);
        if (selectedIndex == -1)
            return; // meaningless click when selected full
        // make copy
        const newSelected = selected.slice();
        const newChoices = choices.slice();
        // move clicked choice to seleceted
        newSelected[selectedIndex] = newChoices[choiceIndex];
        newChoices[choiceIndex] = null
        setSelected(newSelected);
        setChoices(newChoices);
    }

    const handleSelectedClick = (selectedIndex) => {
        if (selected[selectedIndex] === null)
            return; // meaningless click on blank
        // make copy
        const newSelected = selected.slice();
        const newChoices = choices.slice();
        // move selected choice to choices
        const choiceIndex = choices.findIndex(value => value===null);
        newChoices[choiceIndex] = newSelected[selectedIndex];
        newSelected[selectedIndex] = null
        setSelected(newSelected);
        setChoices(newChoices);
    }

    const showSelected = (() => {
        return selected.map((value, i) =>
            <button
                key={i}
                style={{width: '50px', height: '50px'}}
                onClick={() => {
                    handleSelectedClick(i)
                }}
            >
                {value === null? " " : value}
            </button>
        );
    })();

    const showChoices = (() => {
        return choices.map((value, i) =>
            <button
                key={i}
                style={{width: '50px', height: '50px'}}
                onClick={() => {
                    handleChoiceClick(i)
                }}
            >
                {value === null? " " : value}
            </button>
        );
    })();

    return (
        <div className='question-content'>
            <div style={{width: '100%'}}>
                <Question className='use-chinese'>
                    {props.content.question.text}
                </Question>
                <Description>
                    {props.content.description.text}
                </Description>
                <Description>
                    {props.content.title.text}
                </Description>
                <AnswerContainer>
                    {showSelected}
                </AnswerContainer>
                <ChoicesContainer>
                    {showChoices}
                </ChoicesContainer>
                <SubmitContainer>
                    <button
                        className='choice-button'
                    >
                        Skip this term
                    </button>
                    <button
                        className={`choice-button${
                            selected.every(value => value != null) ? ' active' : ''
                        }`}
                        onClick={submitted? props.onActionNext : onSubmit}
                    >
                        {submitted? "Next" : "Submit"}
                    </button>
                </SubmitContainer>
            </div>
        </div>
    );
}

ClickAndDrop.propTypes = {
    content: PropTypes.object.isRequired,
    onActionNext: PropTypes.func.isRequired,
    submitAnswer: PropTypes.func.isRequired,
};