import React from "react";
import "@learning.styles/ItemDisplay.css";
import styled from "styled-components";
import { Word } from "@interfaces/CoreItem";
import RelatedItems from "../RelatedItems";

const SpeakButton = styled.i`
  // display: flex;
  // flex-direction: column;
  float: right;
  font-weight: 200;
  cursor: pointer;
`;

type Props = {
  pinyin: string;
  chinese: string;
  translation: string;
  audioURL: string;
  word: Word;
};

const ExampleSentences = (props: Props): JSX.Element => {
  const audio = new Audio(props.audioURL);

  //Add color to the keyword in sentences
  // const originalpinyin = props.pinyin

  const pinyin = props.pinyin.replace(
    new RegExp("<(.*?)>", "g"),
    "<span class='use-serifs' style='color: #00838F'>$1</span>"
  );

  const chinese = props.chinese.replace(
    new RegExp("<(.*?)>", "g"),
    "<span class='use-serifs' style='color: #00838F'>$1</span>"
  );
  const translation = props.translation.replace(
    new RegExp("<(.*?)>", "g"),
    "<span class='use-serifs' style='color: #00838F'>$1</span>"
  );

  //Output the sentences with HTML <span>
  return (
    <>
      <div className="ExampleCard">
        <SpeakButton className="fas fa-volume" onClick={() => audio.play()} />
        {/* <div>
                {originalpinyin}
            </div> */}
        <div
          className="sentence-pinyin use-chinese"
          dangerouslySetInnerHTML={{ __html: pinyin }}
        />
        <div
          className="sentence-chinese use-chinese"
          dangerouslySetInnerHTML={{ __html: chinese }}
        />
        <div
          className="sentence-translation use-serifs"
          dangerouslySetInnerHTML={{ __html: translation }}
        />
      </div>
    </>
  );
};

export default ExampleSentences;
