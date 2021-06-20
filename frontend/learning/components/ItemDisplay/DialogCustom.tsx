import React, { Component, useState } from "react";
import "@learning.styles/Dialog.css";
import StrokeGif from "./StrokeGif";

import Modal from "react-modal";
import styled from "styled-components";

import "@learning.styles/ItemDisplay.css";
import Constant from "@utils/constant";
import { ItemType } from "@interfaces/CoreItem";

//Styles for Popup
const ModalStyle: Modal.Styles = {
  overlay: {
    backgroundColor: "rgba(116, 116, 116, 0.3)",
  },
  content: {
    position: "absolute",
    top: "10%",
    left: "0px",
    right: "0px",
    height: "500px",
    maxHeight: "100%",
    bottom: "auto",

    display: "inline-block",
    maxWidth: "100%",
    width: "500px",
    margin: "0 auto",

    backgroundColor: "white",
    padding: "25px 50px",

    boxShadow: "2px 2px 6px 2px #30354514",
    borderRadius: "5px",
  },
};

//New 'plus' button
const PlusButton = styled.img`
  position: relative;
  bottom: 100%;
  left: 90%;
  cursor: pointer;
  transform: scale(0.6);
  &:hover {
    transform: scale(0.7);
    transition: 200ms ease-in-out;
  }
`;
//New 'close' button
const CloseButton = styled.i`
  position: relative;
  top: 0;
  left: 100%;
  cursor: grab;
  &:hover {
    transform: scale(1.2);
    transition: 200ms ease-in-out;
  }
`;

const WordContainer = styled.a`
  font-size: 1.75em;
  font-weight: 200;
  text-align: center;
  cursor: pointer;
`;

type Props = {
  item: string;

  type: ItemType;
};

const Dialog = (props: Props): JSX.Element => {
  const type = props.type;
  const item = props.item;
  const [modalState, setModalState] = useState(false);

  Modal.setAppElement(`#${Constant.ROOT_ELEMENT_ID}`);

  const renderItem = (): JSX.Element | null => {
    switch (type) {
      case "word":
        return null;
      case "character":
        return <StrokeGif item={item} />;
      case "radical":
        return null;
    }
  };

  const renderModal = (): JSX.Element | any => {
    return (
      <>
        <div>
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
            {renderItem()}
          </Modal>
        </div>
      </>
    );
  };

  return (
    <>
      <WordContainer
        className="use-chinese"
        onClick={() => setModalState(true)}
      >
        {props.item}
      </WordContainer>
      {renderModal()}
    </>
  );

  // const {modalIsOpen, setModalIsOpen} = props;
  // return(
  //   <>
  //     modalIsOpen ?
  //     <div className="dialog-backdrop">
  //     <div className="dialog-container">
  //       <div className="dialog-header"></div>
  //       <div className="dialpg-body">body</div>
  //       <div className="dialog-footer">
  //         <button className="btn">yes</button>
  //       </div>

  //     </div>

  //   </div>
  //   : null
  //   </>

  // )
};

export default Dialog;
