import React, { Component, isValidElement, useState } from "react";
import "@learning.styles/Dialog.css";
import StrokeGif, {
  WordContainer,
  CharSVGContainer,
  width,
  height,
} from "./StrokeGif";

import Modal from "react-modal";
import styled, { ThemeContext } from "styled-components";

import "@learning.styles/ItemDisplay.css";
import Constant from "@utils/constant";
import { ItemType } from "@interfaces/CoreItem";
import {
  FunctionComponent,
  Children,
  PropsWithChildren,
  ReactElement,
  cloneElement,
} from "react";
import ItemDisplayPopup from "./ItemDisplayPopup";

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

//New 'close' button
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

// don't use div to contain word and pinyin in the same line
const Container = styled.a`
  font-size: 1.75em;
  font-weight: 200;
  text-align: center;
  cursor: pointer;
`;

const BottomContainer = styled.div`
  position relative;
  margin-top: 10px;
  width:auto;
  text-align: center;
  cursor: pointer;
  padding: 20px;
`;

const MoveButton = styled.i`
  position: absolute;
  top: 40%;
  bottom: 40%;
  width: auto;
  cursor: grab;
  font-size: 1.5rem;
  &:hover {
    transform: scale(1.2);
    transition: 200ms ease-in-out;
  }
`;

const LeftMoveButton = styled(MoveButton)`
  left: 10%;
`;

const RightMoveButton = styled(MoveButton)`
  right: 10%;
`;

type Props = {
  item: string;

  type: ItemType | undefined;
};

const Dialog = (props: Props): JSX.Element => {
  const type = props.type;
  const item = props.item;

  const [modalState, setModalState] = useState(false);

  const [indexState, setIndexState] = useState(0);

  // const [lenState, setlenState] = useState(0);

  Modal.setAppElement(`#${Constant.ROOT_ELEMENT_ID}`);

  const renderItem = (): JSX.Element | JSX.Element[] | void[] | null => {
    switch (type) {
      case "word":
        const items = item.split("");
        if (items.length == 0) return null;
        else {
          return items.map((value: string, id: number) => {
            // console.log(value);
            return <StrokeGif item={value} key={id} id={id} />;
          });
        }
      case "character":
        console.log(item);
        return <StrokeGif item={item} />;
      case "radical":
        return null;
      case undefined:
        return null;
    }
  };

  const renderLeftClick = (): void => {
    switch (props.type) {
      case "word":
        const items = props.item.split("");
        return setIndexState((indexState - 1 + items.length) % items.length);
      default:
        return setIndexState(0);
    }
  };

  const renderRightClick = (): void => {
    switch (props.type) {
      case "word":
        const items = props.item.split("");
        return setIndexState((indexState + 1 + items.length) % items.length);
      default:
        return setIndexState(0);
    }
  };

  const renderModal = (): JSX.Element | any => {
    const items = renderItem();

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

          <div
            style={{
              width: "100%",
              height: height,
              whiteSpace: "nowrap",
              overflow: "hidden",
            }}
          >
            <LeftMoveButton
              className="fas fa-angle-left"
              onClick={() => {
                renderLeftClick();
              }}
            />
            <Carousel currentIndex={indexState}>{items}</Carousel>
            <RightMoveButton
              className="fas fa-angle-right"
              onClick={() => {
                renderRightClick();
              }}
            />
          </div>

          <BottomContainer>
            <Container className="use-chinese">{props.item}</Container>
          </BottomContainer>
        </Modal>
      </>
    );
  };

  return (
    <>
      <Container className="use-chinese" onClick={() => setModalState(true)}>
        {props.item}
      </Container>
      {renderModal()}
    </>
  );
};

export default Dialog;

interface CarouselProps {
  currentIndex: number;
}

// interface CarouselState {
//   indexState : number;
// }

class Carousel extends Component<CarouselProps> {
  constructor(props: CarouselProps) {
    super(props);
    // this.state = { indexState: props.currentIndex };
    this.renderChildren = this.renderChildren.bind(this);
    // this.setIndex = this.setIndex.bind(this);
    // this.renderDisplay = this.renderDisplay.bind(this);
  }

  // componentDidUpdate(props:CarouselProps):void {
  //   this.setIndex(props.currentIndex)
  // }

  // componentDidMount():void {
  //   this.setState({indexState:0})
  // }

  renderChildren = (): JSX.Element[] | null | undefined => {
    const { children, currentIndex } = this.props;

    const frameStyle = (display: boolean): React.CSSProperties => ({
      width: width,
      height: height,
      display: display ? "block" : "none",
      position: "relative",
      margin: "auto",
    });

    const len = React.Children.toArray(this.props.children).length;
    return (
      // React.Children.toArray(this.props.children).map(child => {
      React.Children.map(children, (child, index) => {
        const childClone = React.isValidElement(child)
          ? React.cloneElement(child)
          : child;
        return (
          <div
            className="frame"
            style={frameStyle(index >= (this.props.currentIndex + len) % len)}
          >
            {childClone}
          </div>
        );
      })
    );
  };

  render() {
    return <>{this.renderChildren()}</>;
  }
}
