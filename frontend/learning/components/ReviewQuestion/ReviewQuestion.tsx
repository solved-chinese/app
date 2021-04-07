import React from 'react';

import useReviewQuestion from '@learning.hooks/useReviewQuestion';
import MultipleChoice from './MultipleChoice';
import FITBQuestion from './FITBQuestion';
import ClickAndDrop from './ClickAndDrop';
import LoadingView from './LoadingView';

import {
    ReviewQuestionData,
    CNDQuestionContent,
    FITBQuestionContent,
    MCQuestionContent,
    ReviewQuestionAnswer,
    AnswerVerificationResponse
} from '@interfaces/ReviewQuestion';
import {default as oldSubmitAnswer} from '@learning.services/submitAnswer';

type Props = {
    qid?: number,
    question?: ReviewQuestionData,
    submitAnswer?: (answer: ReviewQuestionAnswer) => Promise<AnswerVerificationResponse>,
    onActionNext?: () => void
}

/** 
 * Render a review question view using a ReviewQuestionDescriptor.
 * Review questions have three types: multiple choice (MC), fill
 * in the blank (FITB), and click and drop (CND). Each review
 * question has a submit button. A user cannot resubmit once a
 * question has been submitted. After submission, the user will
 * be shown the correct answer regardless of their choice, and
 * the submit button will display 'next' if props.hasNext == true.
 */
const ReviewQuestion = (props: Props): JSX.Element => {

    const question = props.question ?? useReviewQuestion(`/content/question/${props.qid!}`);

    const submitAnswer = props.submitAnswer ?? ((answer: ReviewQuestionAnswer) =>
        oldSubmitAnswer(props.qid!, '', answer));

    const onActionNext = props.onActionNext ?? (() => window.location.reload());
    
    if (question != null) {
        switch (question.form) {
        case 'MC':
            return <MultipleChoice 
                content={question.content as MCQuestionContent}
                submitAnswer={submitAnswer}
                onActionNext={onActionNext}
            />;
        case 'FITB':
            return <FITBQuestion 
                content={question.content as FITBQuestionContent}
                submitAnswer={submitAnswer}
                onActionNext={onActionNext}
            />;
        case 'CND':
            return <ClickAndDrop
                content={question.content as CNDQuestionContent}
                submitAnswer={submitAnswer}
                onActionNext={onActionNext}
            />;
        default:
            return <LoadingView />;
        }
    } else {
        return <LoadingView />;
    }
};

export default ReviewQuestion;