import React, { useState } from 'react';
import styled from 'styled-components';
import PropTypes from 'prop-types';

import { MCQuestionContent } from '@interfaces/ReviewQuestion';

import submitAnswer from '@learning.services/submitAnswer';

import '@learning.styles/ReviewQuestion.css';

const Context = styled.h1`
    font-size: 1.6em;
    margin-bottom: 40px;
    color: var(--primary-text);
`;

const Question = styled.h2`
    font-size: 1.5em;
    margin-bottom: 30px;
    text-align: center;
    font-weight: 400;
`;

const ChoicesContainer = styled.div`
    display: flex;
    flex-direction: column;
    margin-bottom: 50px;
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
 * Render a multiple choice component.
 * @param {Object} props 
 * @param {MCQuestionContent} props.content
 * @param {Number} props.qid
 * @param {String} props.id
 * 
 * @returns {React.Component} A multiple choice component
 */
export default function MultipleChoice(props) {

    const [selectedAnswer, setSelectedAnswer] = useState(null);

    const [CorrectAnswer, setCorrectAnswer] = useState(null);

    const onSubmit = () => {
        submitAnswer(props.qid, props.id, selectedAnswer).then(response => {
            setCorrectAnswer(response.correct_answer);
        }).catch( msg => {
            console.log(msg);
        });
    };

    const choices = (() => {
        return props.content.choices.map( (v, i) => 
            <button 
                key={v.text}
                className={`choice-button use-serifs${
                    selectedAnswer == i ? ' active' : ''
                }`}
                style={{minWidth: '170px'}}
                onClick={() => {
                    if (selectedAnswer != i) {
                        setSelectedAnswer(i);
                    } else {
                        setSelectedAnswer(null);
                    }
                }}
            >
                {v.text}
            </button>
        );
    })();

    return (
        <div className='question-content'>
            <div style={{width: '100%'}}>
                <Context className='use-chinese'>
                    {props.content.context.text}
                </Context>
                <Question>
                    {props.content.question.text}
                </Question>
                <ChoicesContainer>
                    {choices}
                </ChoicesContainer>
                <SubmitContainer>
                    <button
                        className='choice-button'
                    >
                        I know this
                    </button>
                    <button
                        className={`choice-button${
                            selectedAnswer != null ? ' active' : ''
                        }`}
                        onClick={onSubmit}
                    >
                        Submit
                    </button>
                </SubmitContainer>
            </div>
        </div>
    );
}

MultipleChoice.propTypes = {
    content: PropTypes.object.isRequired,

    id: PropTypes.string.isRequired,

    qid: PropTypes.number.isRequired
};