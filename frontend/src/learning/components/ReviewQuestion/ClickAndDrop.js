import React, { useState } from 'react';
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
 * @param {Number} props.qid
 * @param {String} props.id
 * 
 * @returns {React.Component}
 */
export default function ClickAndDrop(props) {

    const [selectedAnswer, setSelectedAnswer] = useState(null);

    const onSubmit = () => {
        submitAnswer(props.qid, props.id, selectedAnswer).then(response => {
            setCorrectAnswer(response.answer);
        }).catch( msg => {
            console.log(msg);
        });
    };

    const select = (() => {
        var answers = [];
        for(var i=1;i<=parseInt(props.content.answer_length);i++){
            answers.push(' ');
        }
        // console.log(props.content.answer_length);  cannot get answer_length?
        return answers.map( i => 
            <button 
                key={i}
                style={{Width: '50px'}}
                onClick={() => {
                    if (selectedAnswer != i) {
                        setSelectedAnswer(i);
                    } else {    
                        setSelectedAnswer(null);
                    }
                }}
            >
                {i}
            </button>
        );
    })();

    const choices = (() => {
        return props.content.choices.map( i => 
            <button 
                key={i}
                style={{Width: '50px'}}
                onClick={() => {
                    if (selectedAnswer != i) {
                        setSelectedAnswer(i);
                    } else {    
                        setSelectedAnswer(null);
                    }
                }}
            >
                {i}
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
                <ChoicesContainer>
                    {choices}
                </ChoicesContainer>
                <AnswerContainer>
                    {select}
                </AnswerContainer>
                <SubmitContainer>
                    <button
                        className='choice-button'
                    >
                        Skip this term
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

ClickAndDrop.propTypes = {
    content: PropTypes.object.isRequired,

    id: PropTypes.string.isRequired,

    qid: PropTypes.number.isRequired
};