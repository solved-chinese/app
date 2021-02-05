import React, { useState } from 'react';
import styled from 'styled-components';
import PropTypes from 'prop-types';

import { CNDQuestionContent } from '@interfaces/ReviewQuestion';

import submitAnswer from '@learning.services/submitAnswer';

import '@learning.styles/ReviewQuestion.css';

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

/**
 * Render a CND component.
 * @param {Object} props 
 * @param {CNDQuestionContent} props.content
 * @param {Number} props.qid
 * @param {String} props.id
 * 
 * @returns {React.Component}
 */
export default function ClickAndDrop(props) {
    const [selected, setSelected] = useState(Array(props.content.answerLength).fill(null))
    const [choices, setChoices] = useState([...props.content.choices.slice()])
    const [isAnswerCorrect, setIsAnswerCorrect] = useState(null);

    const onSubmit = () => {
        submitAnswer(props.qid, props.id, selected).then(response => {
            setIsAnswerCorrect(response.isCorrect);
        }).catch( msg => {
            console.log(msg);
        });
    };

    var buttonClassName = '';
    if (isAnswerCorrect != null) {
        buttonClassName += isAnswerCorrect ? ' cndCorrect' : ' cndIncorrect';
    }

    const setCorrectAnswer = (correctAnswer) => {
        setSelected(correctAnswer);
    };

    const handleChoiceClick = (choiceIndex) => {
        if (choices[choiceIndex] === null)
            return; // meaningless click on blank
        const selectedIndex = selected.findIndex(value => value===null);
        // make copy
        const newSelected = selected.slice();
        const newChoices = choices.slice();
        // move clicked choice to seleceted
        newSelected[selectedIndex] = newChoices[choiceIndex];
        newChoices[choiceIndex] = null
        setSelected(newSelected);
        setChoices(newChoices);
        if (selectedIndex == props.content.answerLength-1){
            onSubmit();
        } // selected full -> submit
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
            <AnswerButton
                className={buttonClassName}
                key={i}
                onClick={() => {
                    handleSelectedClick(i)
                }}
            >
                {value === null? " " : value}
            </AnswerButton>
        );
    })();

    const showChoices = (() => {
        return choices.map((value, i) =>
            <ChoiceButton
                key={i}
                style={{width: '50px', height: '50px'}}
                onClick={() => {
                    handleChoiceClick(i)
                }}
            >
                {value === null? " " : value}
            </ChoiceButton>
        );
    })();

    var correctResponse = 'Correct!';
    var incorrectResponse = 'Not quite....';

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
                <p className={buttonClassName}>
                    {isAnswerCorrect ? correctResponse : incorrectResponse}
                </p>
            </div>
        </div>
    );
}

ClickAndDrop.propTypes = {
    content: PropTypes.object.isRequired,

    id: PropTypes.string.isRequired,

    qid: PropTypes.number.isRequired
};