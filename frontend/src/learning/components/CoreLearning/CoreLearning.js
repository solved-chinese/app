import React, {useState, useEffect} from 'react';
import PropTypes from 'prop-types';

import ProgressBar from './ProgressBar';
import ItemDisplay from 
    '@learning.components/ItemDisplay/ItemDisplay';
import ReviewQuestion from 
    '@learning.components/ReviewQuestion/ReviewQuestion';

import getLearningNext from '@learning.services/getLearningNext';

import { ReviewQuestionDescriptor } from '@interfaces/ReviewQuestion';
import { ItemDescriptor } from '@interfaces/CoreItem';

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

    const [action, setAction] = useState(props.action);
    const [content, setContent] = useState(props.content);
    const [progressBar, setProgressBar] = useState(props.progressBar);

    const onActionNext = () => {
        getLearningNext();
    };

    const renderItemDisplay = () => (
        <>
            <ProgressBar {...progressBar} />
            <ItemDisplay 
                {...content}
                onActionNext={onActionNext}
            />
        </>
    );

    const renderReviewQuestion = () => (
        <>
            <ProgressBar {...progressBar} />
            <ReviewQuestion 
                {...content} 
                onActionNext={onActionNext}
            />
        </>
    );

    switch (action) {
    case 'review':
        return renderReviewQuestion();
    case 'display':
        return renderItemDisplay();
    default:
        break;
    }
}