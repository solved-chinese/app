import React, {useState, useEffect} from 'react';
import PropTypes from 'prop-types';

import ProgressBar from './ProgressBar';
import ItemDisplay from 
    '@learning.components/ItemDisplay/ItemDisplay';
import ReviewQuestion from 
    '@learning.components/ReviewQuestion/ReviewQuestion';

import { ReviewQuestionDescriptor } from '@interfaces/ReviewQuestion';
import { ItemDescriptor } from '@interfaces/CoreItem';

/**
 * The main component for users' learning experience.
 * @param {Object} props 
 * @param {Object} props.progressBar
 * @param {ReviewQuestionDescriptor | ItemDescriptor} props.content
 * @param {String} props.action
 */
export default function CoreLearning(props) {

    const [action, setAction] = useState(props.action);
    const [content, setContent] = useState(props.content);
    const [progressBar, setProgressBar] = useState(props.progressBar);

    const actionUpdater = (action, content, progressBar) => {
        setAction(action);
        setContent(content);
        setProgressBar(progressBar);
    };

    const renderItemDisplay = () => (
        <>
            <ProgressBar {...progressBar} />
            <ItemDisplay 
                {...content}
                onActionNext={actionUpdater}
            />
        </>
    );

    const renderReviewQuestion = () => (
        <>
            <ProgressBar {...progressBar} />
            <ReviewQuestion 
                {...content} 
                onActionNext={actionUpdater}
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