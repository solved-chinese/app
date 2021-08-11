import React, { useEffect, useState } from "react";
import styled from "styled-components";
import useLoadUser from "../hooks/useLoadUser";
import useLoadClasses from "../hooks/useLoadClass";
import { User } from "@interfaces/User";
import { Class } from "@interfaces/Class";
import PopupModal from "./PopupDisplay/ModalModule";
// import "../styles/DashboardBody.css"

/**
 * The main function that renders the title of dashboard.
 */
const Row = styled.div`
  display: block;
  justify-content: left;
  align-items: center;
  width: 100%;
  height: 300px;
`;

const NameContaner = styled.div`
  position: relative;
  top: 30%;
  left: 30px;
  display: inline-block;
  width: 70%;
`;

const Name = styled.h1`
  font-size: 5em;
  font-weight: 500;
  whilte-spce: nowrap;
`;

const ButtonContainer = styled.div`
  position: relative;
  top: 30%;
  display: inline-block;
`;

export const ButtonClass = styled.button`
  padding: 0.7em 1.2em; /* changed from 0.6em 1.2em */
  border: 1px solid #040302;
  border-radius: 0.25em;
  color: #040302;
  background: white;
  cursor: pointer;
  transition: 150ms ease;
  margin: 0.5em;
  cursor: pointer;

  &.button-primary {
    color: var(--main-theme-color);
    border-color: var(--main-theme-color);
  }

  &:hover {
    color: white;
    background: var(--main-theme-color);
  }

  &.disabled {
    pointer-events: none;
    // background : #BEC0C4;
    border-color: #bec0c4;
    color: #bec0c4;
  }
`;

type NameProps = {
  user: User;

  currentClass: Class | undefined;
};

const NameDisplay = (props: NameProps): JSX.Element => {
  const user = props.user;
  const currentClass = props.currentClass;

  return (
    <Name className="use-chinese">
      {user.displayName}
      {currentClass == null ? "" : "'s " + currentClass.name}
    </Name>
  );
};

type ButtonProps = {
  content: string;
};

type Props = {
  user: User | null;
  currentClass: Class | undefined;
};

const Button = (props: ButtonProps): JSX.Element => {
  return <ButtonClass className="button-primary">{props.content}</ButtonClass>;
};

const Title = (props: Props): JSX.Element => {
  const user = props.user;
  const currentClass = props.currentClass;

  // const user = useLoadUser("/api/accounts/user");

  // const classes = useLoadClasses("/api/classroom/teacher");

  // const [currentClass, setcurrentClass] = useState(classes?.[0])

  // // useEffect to control the async problem
  // useEffect(() => {
  //   setcurrentClass(classes? classes[0]: undefined)
  // }, [classes])

  if (user == null) {
    return <>You need to log in firstly !</>;
  } else {
    return (
      <Row>
        <NameContaner>
          <NameDisplay user={user} currentClass={currentClass} />
        </NameContaner>
        <ButtonContainer>
          <PopupModal event="createClass" />
          {currentClass == undefined ? (
            <></>
          ) : (
            <PopupModal event="editClass" class={currentClass} />
          )}
          {currentClass == undefined ? (
            <></>
          ) : (
            <PopupModal event="addSets" class={currentClass} />
          )}
        </ButtonContainer>
      </Row>
    );
  }
};

export default Title;
