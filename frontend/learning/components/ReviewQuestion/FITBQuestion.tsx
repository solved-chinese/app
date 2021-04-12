import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import {
    AnswerVerificationResponse,
    FITBAnswer,
    FITBQuestionContent,
    ReviewQuestionAnswer
} from '@interfaces/ReviewQuestion';

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

type NextActionCallback = () => void;

type Props = {
    content: FITBQuestionContent,
    submitAnswer: (answer: ReviewQuestionAnswer) => Promise<[AnswerVerificationResponse, NextActionCallback]>,
}

/**
 * Render a fill in the blank (FITB) question.
 * @param {Object} props 
 * @param {FITBQuestionContent} props.content
 * @param {Function} props.submitAnswer
 * @param {Function} props.onActionNext
 * 
 * @returns {React.Component} A FITBQuestion component
 */
const FITBQuestion = (props: Props): JSX.Element => {

    const [answer, setAnswer] = useState<FITBAnswer>('');
    const [correctAnswer, setCorrectAnswer] = useState<FITBAnswer | null>(null);
    const [submitted, setSubmitted] = useState<boolean>(false);
    const [isAnswerCorrect, setIsAnswerCorrect] = useState<boolean | undefined>(undefined);
    const [nextActionCallback, setNextActionCallback] = useState<{ fn: NextActionCallback }>({fn: () => {
        // Do nothing
    }});

    useEffect(() => {
        setAnswer('');
        setCorrectAnswer(null);
        setSubmitted(false);
        setIsAnswerCorrect(undefined);
    }, [props]);

    useEffect(() => {
        if (isAnswerCorrect) {
            const timer = setTimeout(nextActionCallback.fn, 500);
            return () => clearTimeout(timer);
        }
    }, [isAnswerCorrect]);

    const keyListener = (event: KeyboardEvent) => {
        if (event.code === 'Enter' || event.code === 'NumpadEnter') {
            onSubmit();
        }
    };

    useEffect(() => {
        document.addEventListener('keydown', keyListener);
        return () => {document.removeEventListener('keydown', keyListener);};
    }, [submitted, answer]);

    const onSubmit = () => {
        if (submitted) {
            nextActionCallback.fn();
            return;
        }
        if (!answer || answer.length === 0)
            return;
        props.submitAnswer(answer).then(([response, callback]) => {
            setCorrectAnswer(response.answer as FITBAnswer);
            setSubmitted(true);
            setNextActionCallback({fn: callback});
            setIsAnswerCorrect(response.isCorrect);
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
                <Question>{props.content.question}</Question>
                <div className={ inputClassName }>
                    <input
                        autoFocus
                        value={answer}
                        disabled={submitted}
                        className={ 'question-text-field-input use-chinese' }
                        onChange={ e => setAnswer(e.target.value) }
                    />
                    <p className={ responseClassName }>{answerResponse}</p>
                </div>
                <Title 
                    className='use-serifs'
                >
                    {props.content.title}
                </Title>
                <SubmitContainer>
                    <button
                        className={`choice-button${
                            answer != '' ? ' active' : ''
                        }`}
                        hidden={submitted && isAnswerCorrect}
                        disabled={!answer || answer.length === 0}
                        onClick={onSubmit}
                    >
                        {submitted? 'Next' : 'Submit'}
                    </button>
                </SubmitContainer>
                <ResponseContainer>
                    {submitted && <AnswerResponse
                        isCorrect={isAnswerCorrect!}
                        correctAnswer={correctAnswer!}/>}
                </ResponseContainer>
            </div>
        </div>
    );
};

export default FITBQuestion;
