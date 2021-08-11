import React, { Component, useState } from "react";
import Modal from "react-modal";
import styled from "styled-components";

import { Class } from "@interfaces/Class";
import CreateClass from "./CreateClass";
import EditClass from "./EditClass";
import { ButtonClass } from "../Title";
import AddSets from "./AddSets";

//Styles for Popup
const ModalStyle: Modal.Styles = {
  overlay: {
    backgroundColor: "rgba(116, 116, 116, 0.3)",
  },
  content: {
    position: "absolute",
    top: "20%",
    left: "0px",
    right: "0px",
    height: "400px",
    maxHeight: "100%",
    bottom: "auto",

    display: "inline-block",
    maxWidth: "100%",
    width: "400px",
    margin: "0 auto",

    backgroundColor: "white",
    padding: "50px 50px 0px 50px",

    boxShadow: "2px 2px 6px 2px #30354514",
    borderRadius: "5px",
  },
};

// New 'close' button [TODO same with DialogCustom]
// reorganize to new css file
const CloseButton = styled.i`
  position: relative;
  top: 0;
  left: 100%;
  cursor: grab;
  font-size: 1.5rem;
  &:hover {
    transform: scale(1.2);
    transition: 200ms ease-in-out;
  }
`;

const CreateSignal = styled.img`
  position: relative;
  margin-left: 3px;
  margin-right: 5px;
  filter: invert(12%) sepia(69%) saturate(6868%) hue-rotate(7deg)
    brightness(92%) contrast(109%);

  &:hover {
    transform: scale (1.2);
    transition: 200ms ease-in-out;
  }
`;

const Title = styled.h2``;

const NameContainer = styled.a``;

const Container = styled.div``;

const BottomContainer = styled.div``;

type Props = {
  event: "createClass" | "editClass" | "addSets";

  class?: Class;
};

const PopupModal = (props: Props): JSX.Element => {
  const [modalState, setModalState] = useState(false);

  const renderModal = (): JSX.Element => {
    return (
      <>
        <Modal
          closeTimeoutMS={500}
          style={ModalStyle}
          isOpen={modalState}
          onRequestClose={() => setModalState(false)}
        >
          <CloseButton
            className="fas fa-times"
            onClick={() => setModalState(false)}
          />
          <EventTitle event={props.event} />
          <Container>
            <Content event={props.event} class={props.class} />
            <BottomContainer>
              {/* <Option />
                        <Buttons /> */}
            </BottomContainer>
          </Container>
        </Modal>
      </>
    );
  };

  const img = (): JSX.Element => {
    switch (props.event) {
      case "createClass":
        return (
          <CreateSignal
            src="/static/images/small-icons/add_circle_black_24dp.svg"
            width="20px"
          />
        );

      case "addSets":
        return (
          <CreateSignal
            src="/static/images/small-icons/plus_24dp.svg"
            width="20px"
          />
        );
      case "editClass":
        return (
          <CreateSignal
            src="/static/images/small-icons/edit_black_24dp.svg"
            width="20px"
          />
        );

      default:
        return <></>;
    }
  };

  return (
    <>
      <ButtonClass
        onClick={() => setModalState(true)}
        // className={(props.event=="editClass" && props.class==undefined) ? "disabled" : "button-primary"}
        className="button-primary" // using for test TODELETE
      >
        {img()}
        {props.event}
      </ButtonClass>
      {renderModal()}
    </>
  );
};

export default PopupModal;

// const ButtonClass = styled.button`
//   padding: 0.7em 1.2em; /* changed from 0.6em 1.2em */
//   border: 1px solid #040302;
//   border-radius: 0.25em;
//   color: #040302;
//   background: white;
//   cursor: pointer;
//   transition: 150ms ease;
//   margin: 0.5em;

//   &.button-primary {
//     color: var(--main-theme-color);
//     border-color: var(--main-theme-color);
//   }

//   &:hover {
//     color: white;
//     background: var(--main-theme-color);
//   }
// `;

type EventProps = {
  event: "createClass" | "editClass" | "addSets";
};

const EventTitle = (props: EventProps): JSX.Element => {
  const text = (): JSX.Element => {
    switch (props.event) {
      case "createClass":
        return <Title>Create Class</Title>;
      case "editClass":
        return <Title>Edit Class</Title>;
      case "addSets":
        return <Title>Add Sets</Title>;
    }
  };

  return <>{text()}</>;
};

const Content = (props: Props): JSX.Element => {
  const event = props.event;
  const klass = props.class;

  switch (event) {
    case "createClass":
      return <CreateClass />;
    case "editClass":
      return <EditClass class={props.class} />;
    case "addSets":
      return <AddSets className={klass?.name} classpk={klass?.pk} />;
  }
};
