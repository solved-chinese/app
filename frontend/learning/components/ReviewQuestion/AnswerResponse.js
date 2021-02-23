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

/**
 *
 * @param props
 * @param {boolean} props.correct
 * @returns {React.Component}
 */
export default function AnswerResponse(props) {
    const response = (() => {
        if(props.correct)
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
            {response}
        </ResponseContainer>
    )

}