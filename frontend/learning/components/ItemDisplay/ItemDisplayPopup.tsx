import React, { useState } from "react";
import Modal from "react-modal";
import styled from "styled-components";
import CharDisplay from "@learning.components/ItemDisplay/CharacterDisplay/CharDisplay";

import "@learning.styles/ItemDisplay.css";
import Constant from "@utils/constant";
import WordDisplay from "@learning.components/ItemDisplay/WordDisplay/WordDisplay";
import RadDisplay from "@learning.components/ItemDisplay/RadicalDisplay/RadDisplay";
import { ItemType } from "@interfaces/CoreItem";

//Styles for Popup
const ModalStyle: Modal.Styles = {
  overlay: {
    backgroundColor: "rgba(116, 116, 116, 0.3)",
  },
  content: {
    position: "absolute",
    top: "100px",
    left: "0px",
    right: "0px",
    height: "auto",
    maxHeight: "70vh",
    bottom: "auto",

    display: "inline-block",
    maxWidth: "700px",
    width: "100%",
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

type Props = {
  /** URL of the item to be presented in the popup modal. */
  contentURL: string;

  /** The kind of item in contentURL. */
  type: ItemType;
};

/**
 * Renders a component that will bring up a popup modal
 * that displays an item.
 */
const ItemDisplayPopup = (props: Props): JSX.Element => {
  const [ModalState, setModalState] = useState(false);

  console.log(props.contentURL);

  Modal.setAppElement(`#${Constant.ROOT_ELEMENT_ID}`);

  const renderItem = () => {
    switch (props.type) {
      case "word":
        return (
          <WordDisplay url={props.contentURL} autoExpandBreakdown={true} />
        );
      case "character":
        return (
          <CharDisplay url={props.contentURL} autoExpandBreakdown={true} />
        );
      case "radical":
        return <RadDisplay url={props.contentURL} />;
    }
  };

  return (
    <>
      <PlusButton
        src="/static/images/small-icons/read-more-red.svg"
        alt="read more"
        onClick={() => setModalState(true)}
      />

      <div>
        <Modal
          closeTimeoutMS={500}
          style={ModalStyle}
          isOpen={ModalState}
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

export default ItemDisplayPopup;
