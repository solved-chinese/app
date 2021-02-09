import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import PropTypes from 'prop-types';

import { FITBQuestionContent } from '@interfaces/ReviewQuestion';

import submitAnswer from '@learning.services/submitAnswer';

import '@learning.styles/ReviewQuestion.css';
import AnswerResponse from './AnswerResponse';

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

const ResponseContainer = styled.div`
    text-align: center;
`;

/**
 * Render a fill in the blank (FITB) question.
 * @param {Object} props 
 * @param {FITBQuestionContent} props.content
 * @param {Function} props.submitAnswer
 * @param {Function} props.onActionNext
 * 
 * @returns {React.Component} A FITBQuestion component
 */
export default function FITBQuestion(props) {

    const [answer, setAnswer] = useState('');
    const [correctAnswer, setCorrectAnswer] = useState(null);
    const [submitted, setSubmitted] = useState(false);
    const [isAnswerCorrect, setIsAnswerCorrect] = useState(null);

    useEffect(() => {
        setAnswer('');
        setCorrectAnswer(null);
        setSubmitted(false);
        setIsAnswerCorrect(null);
    }, [props])

    const enterListener = event => {
        if (event.code === "Enter" || event.code === "NumpadEnter") {
        onSubmit();
        }
    }

    const onSubmit = () => {
        if (submitted) {
            props.onActionNext();
            return;
        }
        props.submitAnswer(answer).then(response => {
            setCorrectAnswer(response.answer);
            setIsAnswerCorrect(response.isCorrect);
            setSubmitted(true);
        }).catch( msg => {
            console.log(msg);
        });
    };
    let answerResponse = '';
    let inputClassName = 'question-text-field use-chinese';
    let responseClassName = 'answer-response';
    if (isAnswerCorrect != null) {
        inputClassName += isAnswerCorrect ? ' correct' : ' incorrect';
        responseClassName += isAnswerCorrect ? ' correct' : ' incorrect';
        answerResponse = isAnswerCorrect ? '\u{2713}' : '\u{2717}';
    }  
    return (
        <div className='question-content'>
            <div style={{width: '100%'}}>
                <Question>{props.content.question.text}</Question>
                <div className={ inputClassName }>
                    <input
                        autoFocus
                        className={ 'question-text-field-input use-chinese' }
                        onKeyDown={ enterListener }
                        onChange={ e => setAnswer(e.target.value) }
                    ></input>
                    <p className={ responseClassName }>{answerResponse}</p>
                </div>
                <Title 
                    className='use-serifs'
                >
                    {props.content.title.text}
                </Title>
                <SubmitContainer>
                    <button
                        className={`choice-button${
                            answer != '' ? ' active' : ''
                        }`}
                        onClick={onSubmit}
                    >
                        {submitted? 'Next' : 'Submit'}
                    </button>
                </SubmitContainer>
                <ResponseContainer>
                    <p className={ 'answerIncorrect '}>{ isAnswerCorrect !=null ? (isAnswerCorrect ? '' : 'Correct Answer: '+correctAnswer) : ''}</p>
                    {submitted? <AnswerResponse correct={isAnswerCorrect}/> : ""}
                </ResponseContainer>
            </div>
        </div>
    );
}

FITBQuestion.propTypes = {
    content: PropTypes.object.isRequired,
    onActionNext: PropTypes.func.isRequired,
    submitAnswer: PropTypes.func.isRequired,
};