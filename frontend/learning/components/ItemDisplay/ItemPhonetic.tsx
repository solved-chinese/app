import React from "react";
import styled from "styled-components";
import "@learning.styles/ItemDisplay.css";
import StrokeGif from "@learning.components/ItemDisplay/StrokeGif";
import { ItemType } from "@interfaces/CoreItem";
import Dialog from "./DialogCustom";

const Container = styled.div`
  display: inline-block;
  // width: -webkit-fill-available;
  // width : fit-content;
`;

const Phonetic = styled.span`
  text-align: center;
  font-size: 1.5em;
  font-weight: 200;
  white-space: nowrap;
  width : fit-content;
`;

export const SpeakButton = styled.img`
  position: relative;
  margin-left: 3px;
  font-weight: 200; //changed from 200
  cursor: pointer;
  transform: scale(0.6);
  display: inline-block;
`;

const WordContainer = styled.h1`
  font-size: 3.75em;
  font-weight: 200;
  text-align: center;
`;

type Props = {
  type?: ItemType;

  /** Display friendly pinyin. */
  pinyin: string;

  /** The URL of the corresponding audio file. */
  audioURL: string;

  /** The Chinese character to be displayed. */
  item: string;

  /**
   * Indicate whether to enable stroke order.
   * The default is false.
   */
  useStroke?: boolean;
};

/**
 * Renders the Chinese, phonetic(pinyin), and an audio button.
 */
const ItemPhonetic = (props: Props): JSX.Element => {
  const audio = new Audio(props.audioURL);
  // Add slashes at the beginning and the end
  const pinyin = `/${props.pinyin}/`;
  const useStroke = props.useStroke ?? false;
  const type = props.type ?? undefined;

  // const renderWord = () =>
  //   useStroke ? (
  //     <StrokeGif item={props.item} />
  //   ) : (
  //     <WordContainer className="use-chinese">{props.item}</WordContainer>
  //   );

  return (
    <Container>
      <Phonetic className="use-chinese">
        <Dialog item={props.item} type={type} />
        {/* <Pinyin>{pinyin}</Pinyin> */}
        {pinyin}
        <SpeakButton
          src="/static/images/small-icons/pronounce.svg"
          // className='fas fa-volume' // changed to svg
          onClick={() => audio.play()}
        />
      </Phonetic>
      {/* {renderWord()} */}
    </Container>
  );
};

export default ItemPhonetic;
