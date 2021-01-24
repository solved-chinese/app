import React from 'react';

import useReviewQuestion from '@learning.hooks/useReviewQuestion';
import MultipleChoice from './MultipleChoice';

import LoadingView from './LoadingView';

/** 
 * Render a review question view.
 * @returns {?React.Component} Review Question 
 */
export default function ReviewQuestion(props) {
    const qid = props.qid;
    const question = useReviewQuestion(`/content/question/${qid}`);
    
    if (question != null) {
        switch (question.form) {
        case 'MC':
            return <MultipleChoice 
                content={question.content}
                id={qid}
            />;
        default:
            return <LoadingView />;
        }
    } else {
        return <LoadingView />;
    }
}