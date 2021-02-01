import React, { useState } from 'react';
import styled from 'styled-components';
import PropTypes from 'prop-types';

import { FITBQuestionContent } from '@interfaces/ReviewQuestion';

import submitAnswer from '@learning.services/submitAnswer';

import '@learning.styles/ReviewQuestion.css';

const Question = styled.h1`
    font-size: 1.5em;
    margin-bottom: 30px;
    text-align: center;
    font-weight: 600;
`;

const Title = styled.h2`
    font-size: 1.6em;
    text-align: center;
    font-weight: 700;
    margin-bottom: 70px;
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
 * Render a fill in the blank (FITB) question.
 * @param {Object} props 
 * @param {FITBQuestionContent} props.content
 * @param {Number} props.qid
 * @param {String} props.id
 * @param {Boolean} props.hasNext
 * @param {Function} props.onActionNext
 * 
 * @returns {React.Component} A FITBQuestion component
 */
export default function FITBQuestion(props) {

    const [answer, setAnswer] = useState('');

    const [isAnswerCorrect, setIsAnswerCorrect] = useState(null);

    const onSubmit = () => {
        submitAnswer(props.qid, props.id, answer).then(response => {
            setIsAnswerCorrect(response.isCorrect);
        }).catch( msg => {
            console.log(msg);
        });
    };

    var inputClassName = 'question-text-field use-chinese';
    if (isAnswerCorrect != null) {
        inputClassName += isAnswerCorrect ? ' correct' : ' incorrect';
    }

    return (
        <div className='question-content'>
            <div style={{width: '100%'}}>
                <Question>{props.content.question.text}</Question>
                <input 
                    className={ inputClassName } 
                    onChange={ e => setAnswer(e.target.value) }
                ></input>
                <Title 
                    className='use-serifs'
                >
                    {props.content.title.text}
                </Title>
                <SubmitContainer>
                    <button
                        className='choice-button'
                    >
                        Skip this Term
                    </button>
                    <button
                        className={`choice-button${
                            answer != '' ? ' active' : ''
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

FITBQuestion.propTypes = {
    content: PropTypes.object.isRequired,

    qid: PropTypes.number.isRequired,

    id: PropTypes.string.isRequired
};