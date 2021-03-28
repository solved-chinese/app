import React from 'react';

import useReviewQuestion from '@learning.hooks/useReviewQuestion';
import MultipleChoice from './MultipleChoice';
import FITBQuestion from './FITBQuestion';
import ClickAndDrop from './ClickAndDrop';
import LoadingView from './LoadingView';

import {ReviewQuestionDescriptor} from '@interfaces/ReviewQuestion';
import {default as oldSubmitAnswer} from '@learning.services/submitAnswer';

/** 
 * Render a review question view using a ReviewQuestionDescriptor.
 * Review questions have three types: multiple choice (MC), fill
 * in the blank (FITB), and click and drop (CND). Each review
 * question has a submit button. A user cannot resubmit once a
 * question has been submitted. After submission, the user will
 * be shown the correct answer regardless of their choice, and
 * the submit button will display 'next' if props.hasNext == true.
 * 
 * @param { ReviewQuestionDescriptor } props
 * @returns {?JSX.Element} Review Question
 */
export default function ReviewQuestion(props) {
    const question = 'question' in props?
        props.question : useReviewQuestion(`/content/question/${props.qid}`);

    const submitAnswer = 'submitAnswer' in props?
        props.submitAnswer : answer => oldSubmitAnswer(props.qid, '', answer);
    const onActionNext = 'onActionNext' in props?
        props.onActionNext : () => {window.location.reload();};
    
    if (question != null) {
        switch (question.form) {
        case 'MC':
            return <MultipleChoice 
                content={question.content}
                submitAnswer={submitAnswer}
                onActionNext={onActionNext}
            />;
        case 'FITB':
            return <FITBQuestion 
                content={question.content}
                submitAnswer={submitAnswer}
                onActionNext={onActionNext}
            />;
        case 'CND':
            return <ClickAndDrop
                content={question.content}
                submitAnswer={submitAnswer}
                onActionNext={onActionNext}
            />;
        default:
            return <LoadingView />;
        }
    } else {
        return <LoadingView />;
    }
}