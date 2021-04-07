import React, {useState, useEffect} from 'react';
import ProgressBar from './ProgressBar';
import ItemDisplay from
    '@learning.components/ItemDisplay/ItemDisplay';
import ReviewQuestion from
    '@learning.components/ReviewQuestion/ReviewQuestion';

import getLearningNext from '@learning.services/getLearningNext';

import '@learning.styles/CoreLearning.css';
import styled from 'styled-components';
import {
    DisplayObjectContent,
    LearningAction,
    LearningObjectContent,
    ProgressBarData
} from '@interfaces/CoreLearning';
import { ReviewQuestionData } from '@interfaces/ReviewQuestion';

const Title = styled.h1`
    font-size: 2em;
    text-align: center;
    display: block;
    margin-bottom: 25px;
    margin-right: 20px;
    color: var(--primary-text);
`;

const ExitButton = styled.button`
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

type Props = {
    qid: number,
}

/**
 * The main component for users' learning experience. The component
 * will present a set of dynamically determined series of learning 
 * items (i.e. word, character, or radical) and review questions, 
 * and display a progress bar on top that shows the user's mastery 
 * of the current set.
 */
const CoreLearning = (props: Props): JSX.Element => {
    const qid = props.qid;
    const url = `/learning/api/${qid}`;

    const [action, setAction] = useState<LearningAction | null>(null);
    const [content, setContent] = useState<LearningObjectContent | null>(null);
    const [progressBar, setProgressBar] = useState<ProgressBarData | null>(null);
    const [state, setState] = useState<string | undefined>(undefined);

    // FIXME onActionNext is called twice in review, unnecessary
    // FIXME handle conflict

    const onActionNext = (): void => {
        const data = state ? {state} : {};
        getLearningNext(url, data).then(
            response => {
                setAction(response.action);
                setContent(response.content);
                setProgressBar(response.progressBar);
                setState(response.state);
            }
        );
    };

    const submitAnswer = (answer: string) => {
        const data = { answer, state };
        return getLearningNext(url, data);
    };

    useEffect(
        () => {
            onActionNext();
        }, []);

    const renderProgressBar = (progressBar: ProgressBarData) => (
        <div className={'progressBarContainer'}>
            <button
                className={'exitButton'}
                onClick={(e) => {
                    e.preventDefault();
                    window.location.href = `/learning/assignment/${qid}`;
                }}
            > {'\u{2717}'} </button>
            <div className={'progressBar'}>
                <ProgressBar {...progressBar} />
            </div>
        </div>
    );

    const renderItemDisplay = (progressBar: ProgressBarData, content: LearningObjectContent) => (
        <>
            {renderProgressBar(progressBar)}
            <ItemDisplay
                {...content as DisplayObjectContent}
                onActionNext={onActionNext}
            />
        </>
    );

    const renderReviewQuestion = (progressBar: ProgressBarData) => (
        <>
            { renderProgressBar(progressBar) }
            <ReviewQuestion
                question={content as ReviewQuestionData}
                onActionNext={onActionNext}
                submitAnswer={submitAnswer}
            />
        </>
    );

    const renderDoneView = (progressBar: ProgressBarData) => (
        <>
            { renderProgressBar(progressBar) }
            <Title>
                Woohoo! {'\u{1f389}'}
            </Title>
            <Title>
                You&apos;ve completed the assignment :)
            </Title>
            <ExitButton onClick={(e) => {
                e.preventDefault(); window.location.href = '/';}}>
                Return to Dashboard
            </ExitButton>
        </>
    );

    switch (action) {
    case 'review':
        return renderReviewQuestion(progressBar!);
    case 'display':
        return renderItemDisplay(progressBar!, content!);
    case 'done':
        return renderDoneView(progressBar!);
    default:
        return <>loading</>;
    }
};

export default CoreLearning;
