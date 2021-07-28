import React from "react";
import styled from "styled-components";
import useLoadUser from "../hooks/useLoadUser";
import useLoadClasses from "../hooks/useLoadClass";
import { User } from "@interfaces/User";
import { Class } from "@interfaces/Class";
import ModalModule from "./PopupDisplay/ModalModule";
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

const Name = styled.span`
  text-align: center;
  font-size: 3em;
  font-weight: 200;
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

  currentClass: Class | null;

  classes: Class[] | null;
};

const NameDisplay = (props: NameProps): JSX.Element => {
  const user = props.user;
  const currentClass = props.currentClass;

  return (
    <Name>
      {user.displayName}
      {currentClass == null ? "" : "'s " + currentClass.name}
    </Name>
  );
};

type ButtonProps = {
  content: string;
};

const Button = (props: ButtonProps): JSX.Element => {
  return <ButtonClass className="button-primary">{props.content}</ButtonClass>;
};

const Title = (): JSX.Element => {
  const user = useLoadUser("/api/accounts/user");

  const classes = useLoadClasses("/api/classroom/teacher");

  const currentClass = classes ? classes[0] : null;

  if (user == null) {
    return <>You need to log in firstly !</>;
  } else {
    return (
      <Row>
        <NameContaner>
          <NameDisplay
            user={user}
            currentClass={currentClass}
            classes={classes}
          />
        </NameContaner>
        <ButtonContainer>
          <ModalModule event="createClass" />
          <ModalModule event="editClass" />
          <Button content="Add Set" />
        </ButtonContainer>
      </Row>
    );
  }
};

export default Title;
