import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import PropTypes from 'prop-types';

import { MCQuestionContent } from '@interfaces/ReviewQuestion';

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
 * Render a multiple choice (MT) component.
 * @param {Object} props 
 * @param {MCQuestionContent} props.content
 * @param {Function} props.submitAnswer - (answer) => Promise(response)
 * @param {Function} props.onActionNext
 *
 * @returns {React.Component} A multiple choice component
 */
export default function MultipleChoice(props) {

    const [selectedAnswer, setSelectedAnswer] = useState(null);
    const [correctAnswer, setCorrectAnswer] = useState(null);
    const [submitted, setSubmitted] = useState(false);

    useEffect( () => {
        setSelectedAnswer(null);
        setCorrectAnswer(null);
        setSubmitted(false);
    }, [props])

    const onSubmit = () => {
        props.submitAnswer(selectedAnswer).then(response => {
            setCorrectAnswer(response.answer);
            setSubmitted(true);
        }).catch( msg => {
            console.log(msg);
        });
    };

    const getChoiceClassName = value => {
        var name = 'choice-button use-serifs';
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

    const choices = (() => {
        return props.content.choices.map( (v, i) => {
            // support value of either string or object
            var text_value = 'error';
            if (typeof v == 'string')
                text_value = v;
            else if (typeof v == 'object')
                text_value = v.text;

            return (<button
                key={text_value}
                className={getChoiceClassName(text_value)}
                style={{minWidth: '170px'}}
                onClick={!submitted ? (() => {
                    if (selectedAnswer != i) {
                        setSelectedAnswer(text_value);
                    } else {
                        setSelectedAnswer(null);
                    }
                }) : null}
            >
                {text_value}
            </button>)
        }
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
                            selectedAnswer != null || submitted ? ' active' : ''
                        }`}
                        onClick={submitted ? props.onActionNext : onSubmit }
                    >
                        {submitted ? 'Next' : 'Submit' }
                    </button>
                </SubmitContainer>
            </div>
        </div>
    );
}

MultipleChoice.propTypes = {
    content: PropTypes.object.isRequired,

    submitAnswer: PropTypes.func.isRequired,

    onActionNext: PropTypes.func.isRequired,
};