import React, {useState, useEffect} from 'react';
import ProgressBar from './ProgressBar';
import ItemDisplay from 
    '@learning.components/ItemDisplay/ItemDisplay';
import ReviewQuestion from 
    '@learning.components/ReviewQuestion/ReviewQuestion';

import getLearningNext from '@learning.services/getLearningNext';

import { ItemDescriptor } from '@interfaces/CoreItem';

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


import '@learning.styles/CoreLearning.css';
import styled from "styled-components";
/**
 * The main component for users' learning experience. The component
 * will present a set of dynamically determined series of learning 
 * items (i.e. word, character, or radical) and review questions, 
 * and display a progress bar on top that shows the user's mastery 
 * of the current set.
 * 
 * @param {Object} props
 * @param {Object} props.progressBar
 * @param {ReviewQuestionDescriptor | ItemDescriptor} props.content
 * @param {String} props.action
 */
export default function CoreLearning(props) {
    const qid = props.qid;
    const url = `/learning/api/${qid}`;

    const [action, setAction] = useState(null);
    const [content, setContent] = useState(null);
    const [progressBar, setProgressBar] = useState(null);
    const [state, setState] = useState(null);

    // FIXME onActionNext is called twice in review, unnecessary
    // FIXME handle conflict

    const onActionNext = () => {
        const data = {};
        if (state != null)
            data.state = state;
        getLearningNext(url, data).then(
            response => {
                setAction(response.action);
                setContent(response.content);
                setProgressBar(response.progressBar);
                setState(response.state);
            }
        );
    };

    const submitAnswer = (answer) => {
        const data = {
            answer: answer
        };
        if (state != null)
            data.state = state;
        return getLearningNext(url, data);
    };

    useEffect(
        () => {
            onActionNext();
        }, []);

    const renderProgressBar = () => (
        <div className={'progressBarContainer'}>
            <button className={'exitButton'} onClick={(e) => { e.preventDefault(); window.location.href = `/learning/assignment/${qid}`;}}> {'\u{2717}'} </button>
            <div className={'progressBar'}>
                <ProgressBar {...progressBar} />
            </div>
        </div>
    );

    const renderItemDisplay = () => (
        <>
            {renderProgressBar()}
            <ItemDisplay
                {...content}
                onActionNext={onActionNext}
            />
        </>
    );

    const showAssignmentPage = () => {
        props.history.push(`/learning/assignment/${qid}`);
    };

    const renderReviewQuestion = () => (
        <>
            {renderProgressBar()}
            <ReviewQuestion
                question={content}
                onActionNext={onActionNext}
                submitAnswer={submitAnswer}
            />
        </>
    );

    const renderDoneView = () => (
        <>
            {renderProgressBar()}
            <Title>
                Woohoo! {"\u{1f389}"}
            </Title>
            <Title>
                You've completed the assignment :)
            </Title>
            <ExitButton onClick={(e) => {
                e.preventDefault(); window.location.href = `/`;}}>
                Return to Dashboard
            </ExitButton>
        </>
    );

    switch (action) {
    case 'review':
        return renderReviewQuestion();
    case 'display':
        return renderItemDisplay();
    case 'done':
        return renderDoneView();
    default:
        return 'loading';
    }
}