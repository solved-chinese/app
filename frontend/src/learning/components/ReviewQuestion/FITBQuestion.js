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

const TextField = styled.input`
    width: 200px;
    height: 2em;
    margin: auto;
    display: block;
    margin-bottom: 30px;
    border: none;
    text-align: center;

    font-size: 1.5em;

    border-top-left-radius: 5px;
    border-top-right-radius: 5px;

    border-bottom: 1.5px solid #bec0c4;
    background-color: #ebebeb;

    :focus {
        outline: none;
    }
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
 * Return a fill in the blank question.
 * @param {Object} props 
 * @param {FITBQuestionContent} props.content
 * @param {Number} props.qid
 * @param {String} props.id
 * 
 * @returns {React.Component} A FITBQuestion component
 */
export default function FITBQuestion(props) {

    const [answer, setAnswer] = useState('');

    const onSubmit = () => {
        submitAnswer(props.qid, props.id, answer).then(response => {

        }).catch( msg => {
            console.log(msg);
        });
    };

    return (
        <div className='question-content'>
            <div style={{width: '100%'}}>
                <Question>{props.content.question.text}</Question>
                <TextField 
                    className='use-chinese'
                    onChange={ e => setAnswer(e.target.value) }
                ></TextField>
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