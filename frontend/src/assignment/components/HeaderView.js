import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';

const Title = styled.h1`
    font-size: 2em;
    display: inline-block;
    margin-bottom: 25px;
    margin-right: 20px;
    color: var(--primary-text);
`;

const DueLabel = styled.h3`
    font-size: 1.3em;
    font-weight: 600;
    margin-bottom: 25px;
    display: inline-block;
    color: var(--secondary-text);
`;

const CompleteButton = styled.button`
    display: block;
    border: 1px solid var(--main-theme-color);
    color: var(--main-theme-color);
    background-color: white;
    padding: 0.4em 2em;
    margin-bottom: 25px;
    transition: all 150ms ease-in-out;
    border-radius: 3px;
    font-size: 0.9em;
  
    &:hover {
        background-color: var(--main-theme-color);
        color: white;
    }
`;

export default function HeaderView(props) {
    return (
        <>
            <Title className='use-serifs'>Integrated Chinese Lv1 Ls1</Title>
            <DueLabel>Due Monday 1/4</DueLabel>
            <CompleteButton>Complete Assignment</CompleteButton>
        </>
    );
}