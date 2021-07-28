import React from "react";

import useReviewQuestion from "@learning.hooks/useReviewQuestion";
import MultipleChoice from "./MultipleChoice";
import FITBQuestion from "./FITBQuestion";
import ClickAndDrop from "./ClickAndDrop";
import LoadingView from "./LoadingView";

import {
  ReviewQuestionData,
  CNDQuestionContent,
  FITBQuestionContent,
  MCQuestionContent,
  ReviewQuestionAnswer,
  AnswerVerificationResponse,
} from "@interfaces/ReviewQuestion";
import submitAnswer from "@learning.services/submitAnswer";

type NextActionCallback = () => void;

type Props = {
  qid?: number;
  question?: ReviewQuestionData;
  submitAnswer?: (
    answer: ReviewQuestionAnswer
  ) => Promise<[AnswerVerificationResponse, NextActionCallback]>;
  onActionNext?: () => void;
};

/**
 * Render a review question view using a either the qid or the
 * question props. The question prop takes precedence over the qid.
 * A submit answer handler can be passed in optionally, which, upon
 * subviews submitting the answer, returns a promise containing the
 * correct answer info as well as a callback function for the
 * next action. If submit answer is not passed in with props, as in
 * the case when ReviewQuestion is rendered individually from url
 * instead of by CoreLearning, a handler function will be created
 * from learning/service/submitAnswer.ts, and the completion function
 * will be set to refresh the window.
 */
const ReviewQuestion = (props: Props): JSX.Element => {
  const question =
    props.question ?? useReviewQuestion(`/api/content/question/${props.qid!}`);

  const submitAnswerFn: (
    answer: ReviewQuestionAnswer
  ) => Promise<[AnswerVerificationResponse, NextActionCallback]> =
    props.submitAnswer ??
    ((answer: ReviewQuestionAnswer) =>
      submitAnswer(props.qid!, "", answer, () => {
        window.location.reload();
      }));

  if (question != null) {
    switch (question.form) {
      case "MC":
        return (
          <MultipleChoice
            content={question.content as MCQuestionContent}
            submitAnswer={submitAnswerFn}
          />
        );
      case "FITB":
        return (
          <FITBQuestion
            content={question.content as FITBQuestionContent}
            submitAnswer={submitAnswerFn}
          />
        );
      case "CND":
        return (
          <ClickAndDrop
            content={question.content as CNDQuestionContent}
            submitAnswer={submitAnswerFn}
          />
        );
      default:
        return <LoadingView />;
    }
  } else {
    return <LoadingView />;
  }
};

export default ReviewQuestion;
