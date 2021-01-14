import React from 'react';
import styled from 'styled-components';
import PropTypes from 'prop-types';

import { MCQuestionContent } from '@interfaces/ReviewQuestion';

import '@learning.styles/ReviewQuestion.css';

const ContentWrapper = styled.div`
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    max-width: 800px;
    height: 65vh;
    overflow: hidden;
    margin: auto;
    padding-top: 50px;
`;

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
`;

/**
 * Render a multiple choice component.
 * @param {Object} props 
 * @param {MCQuestionContent} props.content
 * 
 * @returns {React.Component} A multiple choice component
 */
export default function MultipleChoice(props) {

    const choices = (() => {
        return props.content.choices.map( v => 
            <button 
                key={v.text}
                className='choice-button use-serifs'
            >
                {v.text}
            </button>
        );
    })();

    console.log(choices);

    return (
        <ContentWrapper>
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
            </div>
        </ContentWrapper>
    );
}

MultipleChoice.propTypes = {
    content: PropTypes.object.isRequired
};