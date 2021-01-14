import React from 'react';
import styled from 'styled-components';
import PropTypes from 'prop-types';

import { MCQuestionContent } from '@interfaces/ReviewQuestion';

const ContentWrapper = styled.div`
    display: flex;
    align-items: center;
    width: 100%;
    max-width: 800px;
    height: 65vh;
    overflow: hidden;
    margin: auto;
    padding-top: 50px;
`;

const Context = styled.h2`
    font-size: 1.6em;
    margin-bottom: 40px;
    color: var(--secondary-text);
`;

const Question = styled.h1`
    font-size: 1.6em;
    margin-bottom: 40px;
    text-align: center;
    font-weight: 400;
`;

/**
 * Render a multiple choice component.
 * @param {Object} props 
 * @param {MCQuestionContent} props.content
 * 
 * @returns {React.Component} A multiple choice component
 */
export default function MultipleChoice(props) {
    return (
        <ContentWrapper>
            <div style={{width: '100%'}}>
                <Context className='use-chinese'>
                    {props.content.context.text}
                </Context>
                <Question>
                    {props.content.question.text}
                </Question>
            </div>
        </ContentWrapper>
    );
}

MultipleChoice.propTypes = {
    content: PropTypes.object.isRequired
};