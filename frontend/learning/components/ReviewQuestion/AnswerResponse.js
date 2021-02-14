import React from 'react';
import styled from 'styled-components';

import '@learning.styles/ReviewQuestion.css';


const { array } = require("prop-types");

const correctResponse = new Array(
    'Good job! \u{1F389}',
    'Correct! \u{1F3C6}',
    'Nice work! \u{1F973}',
    'Lets go \u{1F929}'
);

const incorrectResponse = new Array(
    'Uh oh, try again \u{1F389}',
    'Not quite... \u{1F914}',
    'Ah, almost there! \u{1F62B}',
    'Try again, you got this! \u{1F389}'
);

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