import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import PropTypes from 'prop-types';

import { MCQuestionContent } from '@interfaces/ReviewQuestion';
import AnswerResponse from './AnswerResponse';
import { getTextAudio } from './utils';
import { SpeakButton} from "@learning.components/ItemDisplay/ItemPhonetic";


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
    const [isAnswerCorrect, setIsAnswerCorrect] = useState(null);

    useEffect( () => {
        setSelectedAnswer(null);
        setCorrectAnswer(null);
        setSubmitted(false);
        setIsAnswerCorrect(null);
    }, [props])

    useEffect(() => {
        if (selectedAnswer && !submitted)
            onSubmit();
    }, [selectedAnswer])

    useEffect(() => {
        if (isAnswerCorrect) {
            const timer = setTimeout(() => {props.onActionNext();}, 500);
            return () => clearTimeout(timer);
        }
    }, [isAnswerCorrect])

    const onSubmit = () => {
        props.submitAnswer(selectedAnswer).then(response => {
            setCorrectAnswer(response.answer);
            setSubmitted(true);
            setIsAnswerCorrect(response.isCorrect);
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
            let [text, audio] = getTextAudio(v);
            return (
                <>
                    <button
                    key={text}
                    className={getChoiceClassName(text)}
                    style={{minWidth: '170px'}}
                    onClick={!submitted ? (() => {
                        if (selectedAnswer != i) {
                            setSelectedAnswer(text);
                        } else {
                            setSelectedAnswer(null);
                        }}) : null}
                    >
                        {text}
                    </button>
                    {audio? <SpeakButton
                        src="/static/images/small-icons/pronounce.svg"
                        onClick={() => new Audio(audio).play()}/> : null}
                </>
            )
        }
        );
    })();

    return (
        <div className='question-content'>
            <div style={{width: '100%'}}>
                <Context className='use-chinese'>
                    {(() => {
                        let [text, audio] = getTextAudio(props.content.context);
                        return (<>
                            {text}
                            {audio? <SpeakButton
                                src="/static/images/small-icons/pronounce.svg"
                                onClick={() => new Audio(audio).play()}/> : null}
                        </>)
                    })()}
                </Context>
                <Question>
                    {(() => {
                        let [text, audio] = getTextAudio(props.content.question);
                        return (<>
                            {text}
                            {audio? <SpeakButton
                                src="/static/images/small-icons/pronounce.svg"
                                onClick={() => new Audio(audio).play()}/> : null}
                        </>)
                    })()}
                </Question>
                <ChoicesContainer>
                    {choices}
                </ChoicesContainer>
                <SubmitContainer>
                    <button
                        className="choice-button"
                        hidden={!submitted || (submitted && isAnswerCorrect)}
                        onClick={props.onActionNext}
                    >
                        Next
                    </button>
                </SubmitContainer>
                {submitted? <AnswerResponse correct={selectedAnswer==correctAnswer}/> : ""}
            </div>
        </div>
    );
}

MultipleChoice.propTypes = {
    content: PropTypes.object.isRequired,

    submitAnswer: PropTypes.func.isRequired,

    onActionNext: PropTypes.func.isRequired,
};
