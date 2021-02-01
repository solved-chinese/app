import React from 'react';

import useReviewQuestion from '@learning.hooks/useReviewQuestion';
import MultipleChoice from './MultipleChoice';
import FITBQuestion from './FITBQuestion';

import LoadingView from './LoadingView';

import {ReviewQuestionDescriptor} from '@interfaces/ReviewQuestion';

/** 
 * Render a review question view.
 * @param { ReviewQuestionDescriptor } props
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
                hasNext={props.hasNext}
                onActionNext={props.onActionNext}
            />;
        case 'FITB':
            return <FITBQuestion 
                content={question.content}
                qid={qid}
                id={question.id}
                hasNext={props.hasNext}
                onActionNext={props.onActionNext}
            />;
        default:
            return <LoadingView />;
        }
    } else {
        return <LoadingView />;
    }
}