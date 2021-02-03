import React from 'react';

import useReviewQuestion from '@learning.hooks/useReviewQuestion';
import MultipleChoice from './MultipleChoice';
import FITBQuestion from './FITBQuestion';
import ClickAndDrop from './ClickAndDrop';
import LoadingView from './LoadingView';

import {ReviewQuestionDescriptor} from '@interfaces/ReviewQuestion';

/** 
 * Render a review question view using a ReviewQuestionDescriptor.
 * Review questions have three types: multiple choice (MT), fill
 * in the blank (FITB), and click and drop (CND). Each review
 * question has a submit button. A user cannot resubmit once a
 * question has been submitted. After submission, the user will
 * be shown the correct answer regardless of their choice, and
 * the submit button will display 'next' if props.hasNext == true.
 * 
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
        case 'CND':
            return <ClickAndDrop
                content={question.content}
                qid={qid}
                id={question.id}
            />;
        default:
            return <LoadingView />;
        }
    } else {
        return <LoadingView />;
    }
}