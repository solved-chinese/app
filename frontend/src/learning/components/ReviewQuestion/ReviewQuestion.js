import React from 'react';

import useReviewQuestion from '@learning.hooks/useReviewQuestion';
import MultipleChoice from './MultipleChoice';
import FITBQuestion from './FITBQuestion';

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
                qid={qid}
                id={question.id}
            />;
        case 'FITB':
            return <FITBQuestion 
                content={question.content}
            />;
        default:
            return <LoadingView />;
        }
    } else {
        return <LoadingView />;
    }
}