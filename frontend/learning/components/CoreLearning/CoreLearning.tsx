import React, { useState, useEffect } from "react";
import ProgressBar from "./ProgressBar";
import Constant from "@utils/constant";
import ItemDisplay from "@learning.components/ItemDisplay/ItemDisplay";
import ReviewQuestion from "@learning.components/ReviewQuestion/ReviewQuestion";

import getLearningNext from "@learning.services/getLearningNext";

import "@learning.styles/CoreLearning.css";
import styled from "styled-components";
import {
  AnswerSubmitResponse,
  LearningNextResponse,
  ProgressBarData,
} from "@interfaces/CoreLearning";
import {
  ReviewQuestionAnswer,
  ReviewQuestionData,
} from "@interfaces/ReviewQuestion";
import { DisplayObjectContent } from "@interfaces/CoreItem";

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

type Props = {
  qid: number;
};

const BonusText = styled.h2`
  margin-top: 25px;
  margin-bottom: -30px;
`;

// so that next button and bonus texts align with content card
const LearningContentContainer = styled.div`
  max-width: 800px;
  width: 100%;
  margin: auto;
`;

/**
 * The main component for users' learning experience. The component
 * will present a set of dynamically determined series of learning
 * items (i.e. word, character, or radical) and review questions,
 * and display a progress bar on top that shows the user's mastery
 * of the current set.
 */
const CoreLearning = (props: Props): JSX.Element => {
  const qid = props.qid;
  const url = `/learning/api/${qid}`;

  type LearningState = LearningNextResponse;
  const [learningState, setLearningState] = useState<LearningState>();

  useEffect(() => {
    // make progress bar occupy header position
    document.getElementById(Constant.HEADER_ELEMENT_ID)!.style.display = "none";
    document.getElementById(Constant.ROOT_ELEMENT_ID)!.style.marginTop =
      "-70px";
  }, []);

  const onActionNext = () => {
    const data = learningState?.state ? { state: learningState.state } : {};
    getLearningNext(url, data).then((response) => {
      setLearningState(response);
    });
  };

  type ActionNextCallback = () => void;

  const submitAnswer = (
    answer: ReviewQuestionAnswer
  ): Promise<[AnswerSubmitResponse, ActionNextCallback]> => {
    const data = { answer, state: learningState!.state };
    return (getLearningNext(url, data) as Promise<AnswerSubmitResponse>).then(
      (response) => {
        const callback: ActionNextCallback = () => {
          setLearningState(response);
        };
        return [response, callback];
      }
    );
  };

  useEffect(() => {
    onActionNext();
  }, []);

  const renderProgressBar = (progressBar: ProgressBarData) => (
    <div className={"progressBarContainer"}>
      <button
        className={"exitButton"}
        onClick={(e) => {
          e.preventDefault();
          window.location.href = `/api/learning/assignment/${qid}`;
        }}
      >
        {" "}
        {"\u{2717}"}{" "}
      </button>
      <div className={"progressBar"}>
        <ProgressBar {...progressBar} />
      </div>
    </div>
  );

  const renderBonus = (learningState: LearningState) => {
    if ((learningState.content as DisplayObjectContent).type !== undefined) {
      const type = (learningState.content as DisplayObjectContent).type;
      if (type == "radical")
        return <BonusText>Bonus Radical! {"\u{1F609}"}</BonusText>;
      else if (type == "character")
        return <BonusText>Bonus Character! {"\u{1F60F}"}</BonusText>;
      return null;
    }
  };

  const renderItemDisplay = (learningState: LearningState) => (
    <>
      {renderProgressBar(learningState.progressBar)}
      <LearningContentContainer>
        {renderBonus(learningState)}
        <ItemDisplay
          {...(learningState.content as DisplayObjectContent)}
          onActionNext={onActionNext}
        />
      </LearningContentContainer>
    </>
  );

  const renderReviewQuestion = (learningState: LearningState) => (
    <>
      {renderProgressBar(learningState.progressBar)}
      <ReviewQuestion
        question={learningState.content as ReviewQuestionData}
        submitAnswer={submitAnswer}
      />
    </>
  );

  const renderDoneView = (progressBar: ProgressBarData) => (
    <>
      {renderProgressBar(progressBar)}
      <Title>Woohoo! {"\u{1f389}"}</Title>
      <Title>You&apos;ve completed the assignment :)</Title>
      <ExitButton
        onClick={(e) => {
          e.preventDefault();
          window.location.href = "/";
        }}
      >
        Return to Dashboard
      </ExitButton>
    </>
  );

  switch (learningState?.action) {
    case "review":
      return renderReviewQuestion(learningState);
    case "display":
      return renderItemDisplay(learningState);
    case "done":
      return renderDoneView(learningState.progressBar);
    default:
      return <>loading</>;
  }
};

export default CoreLearning;
