import React, { Component, isValidElement, useState } from "react";
import "@learning.styles/Dialog.css";
import StrokeGif,{WordContainer,CharSVGContainer, width,height} from "./StrokeGif";

import Modal from "react-modal";
import styled from "styled-components";

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
  top : 40%;
  bottom : 40%;
  width:auto;
  cursor: grab;
  font-size: 1.5rem;
  &:hover {
    transform: scale(1.2);
    transition: 200ms ease-in-out;
  }
`;

const LeftMoveButton = styled(MoveButton)`
  left:10%;
`;

const RightMoveButton = styled(MoveButton)`
  right:10%;
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
        return <StrokeGif item={item} />;
      case "character":
        return <StrokeGif item={item} />;
      case "radical":
        return null;
    }
  };


  // const renderChildren = ():JSX.Element => {
  //   const children = props;
  
  //   return React.Children.map(children：JSX.Element[], child => {
          
  //     const childClone = React.cloneElement(child as unknown as JSX.Element);
  //     return (
  //         {childClone}
  //     );
  //   });
  
  // }
    
  // }

  const items = renderItem();

  const renderModal = (): JSX.Element | any => {
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
          <Carousel item='test'>
          {items}
          </Carousel>
          
          <BottomContainer>
            <Container className="use-chinese">{props.item}</Container>
          </BottomContainer>
        </Modal>
      </>
    );
  };




  return (
    <>
      <Container
        className="use-chinese"
        onClick={() => setModalState(true)}
      >
        {props.item}
      </Container>
      {renderModal()}
    </>
  );
};

export default Dialog;

interface CarouselProps {
  item : string;
}

class Carousel extends Component <CarouselProps> {
  constructor(props:CarouselProps){
    super(props);
    this.state = { currentIndex: 0 };
    this.renderChildren = this.renderChildren.bind(this);
    this.setIndex = this.setIndex.bind(this);
  }

  renderChildren = () : JSX.Element[] | null | undefined => {
    const {children,item}= this.props
    // console.log(children)


    const frameStyle = ():React.CSSProperties=> ({
      width : width,
      height : height,
      whiteSpace: 'nowrap',
      overflow: 'hidden',
      position: 'relative',
      margin: 'auto'
    })

    // const buttonStyle = {
    //   position: 'absolute',
    //   top: '40%',
    //   bottom: '40%',
    //   width: '10%',
    //   background: 'rgba(0,0,0,0.2)',
    //   outline: 'none',
    //   border: 'none'
    // };

    // const leftButtonStyle = {
    //   ...buttonStyle,
    //   left: 0
    // };

    // const rightButtonStyle = {
    //   ...buttonStyle,
    //   right: 0
    // };

    return (
      // React.Children.toArray(this.props.children).map(child => {

      React.Children.map(children,child => {

      const childClone = React.isValidElement(child) ? React.cloneElement(child) : child;
      console.log(childClone);
      return (
        <div style={{width:'100%'}}>
        <LeftMoveButton
        className="fas fa-angle-left"
        onClick={()=>{}}
        />
        <div className="frame" style={frameStyle ()}>
          {childClone}
        </div>
        
        <RightMoveButton
        className="fas fa-angle-right"
        onClick={()=>{}}/>
        </div>
      );
    })
    )
  }

  setIndex(index:number) {
    const len = React.Children.toArray(this.props.children).length;
    const nextIndex = (index + len) % len;
    this.setState({ currentIndex: nextIndex });
  }

  render() {
    const item = this.props.item

    // const offset = -currentIndex * width;
    // const frameStyle = {
    //   width: width,
    //   height: height,
    //   whiteSpace: 'nowrap',
    //   overflow: 'hidden',
    //   position: 'relative'
    // };

    // const imageRowStyle = {
    //   marginLeft: offset,
    //   transition: '.2s'
    // };

    // const buttonStyle = {
    //   position: 'absolute',
    //   top: '40%',
    //   bottom: '40%',
    //   width: '10%',
    //   background: 'rgba(0,0,0,0.2)',
    //   outline: 'none',
    //   border: 'none'
    // };

    // const leftButtonStyle = {
    //   ...buttonStyle,
    //   left: 0
    // };

    // const rightButtonStyle = {
    //   ...buttonStyle,
    //   right: 0
    // };
    return (
      <>
        
        {this.renderChildren ()}

      </>
      // <div className="carousel">
      //   <div className="frame" style={frameStyle}>
      //     <button
      //       onClick={() => this.setIndex(currentIndex - 1)}
      //       style={leftButtonStyle}
      //     >
      //       &lt;
      //     </button>
      //     <div style={imageRowStyle}>{this.renderChildren()}</div>
      //     <button
      //       onClick={() => this.setIndex(currentIndex + 1)}
      //       style={rightButtonStyle}
      //     >
      //       &gt;
      //     </button>
      //   </div>
      // </div>
    );
  }

}
