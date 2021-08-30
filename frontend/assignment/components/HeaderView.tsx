import React from "react";
import styled from "styled-components";

const Title = styled.h1`
  font-size: 2em;
  display: inline-block;
  margin-bottom: 25px;
  margin-right: 20px;
  color: var(--primary-text);
`;

// we are not doing due date this patch
// const DueLabel = styled.h3`
//     font-size: 1.3em;
//     font-weight: 600;
//     margin-bottom: 25px;
//     display: inline-block;
//     color: var(--secondary-text);
// `;

const CompleteButton = styled.button`
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

const BackButton = styled.button`
  display: flex;
  align-items: center;
  width: 100%;
  color: gray;
  padding: 10px 0;
  border: none;
  background: none;
`;

type Props = {
  name: string;
  onActionComplete: () => void;
};

const HeaderView = (props: Props): JSX.Element => {
  return (
    <>
      <BackButton
        onClick={() => {
          window.location.href = "/";
        }}
      >
        {" "}
        &lt; Back to Dashboard{" "}
      </BackButton>
      <Title className="use-serifs">{props.name}</Title>
      <CompleteButton onClick={props.onActionComplete}>
        View Practice Question
      </CompleteButton>
    </>
  );
};

export default HeaderView;
