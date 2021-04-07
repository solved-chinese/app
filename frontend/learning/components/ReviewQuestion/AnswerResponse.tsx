import React from 'react';
import styled from 'styled-components';

import '@learning.styles/ReviewQuestion.css';


const correctResponse = [
    'Good job! \u{1F389}',
    'Correct! \u{1F3C6}',
    'Nice work! \u{1F973}',
    'Let\'s go \u{1F929}',
];

const incorrectResponse = [
    'Uh oh, review this one \u{1F623}',
    'Not quite... \u{1F914}',
    'Almost there! \u{1F62B}',
    'You\'ll get it next time! \u{1F389}',
];

const ResponseContainer = styled.div`
    text-align: center;
`;

const AnswerIncorrect = styled.span`
    color:rgb(238,109,0);
`;

const CorrectAnswer = styled.span`
    color:rgb(103,158,59);
`;

type Props = {
    isCorrect: boolean,
    correctAnswer: string
}

const AnswerResponse = (props: Props): JSX.Element => {
    const correctAnswer = (() => {
        if (!props.isCorrect && props.correctAnswer) {
            return (
                <>
                    <AnswerIncorrect>Correct Answer: </AnswerIncorrect>
                    <CorrectAnswer>{props.correctAnswer}</CorrectAnswer>
                </>
            );
        }
    })();

    const response = (() => {
        if(props.isCorrect)
            return (
                <p className='answerCorrect'>
                    {correctResponse[Math.floor(Math.random() * correctResponse.length)]}
                </p>
            );
        else
            return (
                <p className='answerIncorrect'>
                    {incorrectResponse[Math.floor(Math.random() * incorrectResponse.length)]}
                </p>
            );
    })();

    return (
        <ResponseContainer>
            {correctAnswer}
            {response}
        </ResponseContainer>
    );

};

export default AnswerResponse;