import React from "react";
import styled from "styled-components";

import WordDefinition from "./WordDefinition";
import ExampleSentences from "./ExampleSentences";

import BreakdownView from "@learning.components/ItemDisplay/BreakdownView";
import LoadingView from "@learning.components/ItemDisplay/LoadingView";
import useLoadWord from "@learning.hooks/useLoadWord";

import { Word } from "@interfaces/CoreItem";
import RelatedItems from "../RelatedItems";

//Top and Bottom Containers
const ContainerTop = styled.div`
  display: inline-block;
  // width: 100%;
  justify-content: start;
  align-items: center;
  // @media only screen and (max-width: 480px) {
  //     flex-direction: row;
  // }
`;

const ContainerRight = styled.div`
  display: block;
`;

const ContainerRightTop = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  @media only screen and (max-width: 1000px) {
    flex-direction: row;
  }
`;

const ContainerInside = styled.div`
  display: inline-block;
  justify-content: center;
  align-items: center;
  max-width: 768px;
`;

const ExampleSentenceHeading = styled.h2`
  color: var(--teritary-text);
  margin-top: 10px;
  font-size: 0.9em;
  font-weight: 400;
  text-align: center;
`;

const MemoryAidHeading = styled.h2`
  display: inline-block;
  width: 100%;
  color: #bec0c4;
  letter-spacing: 0.6px;
  font-size: 0.9em;
  font-weight: 500;
  text-align: center;
  margin: 20px auto 10px;
`;

const MemoryAidContent = styled.div`
  width: 100%;
  font-size: 0.9em;
  color: var(--secondary-text);
  border-radius: 5px;
  padding: 15px 20px;
  font-weight: 400;
  background-color: lightgrey;
`;

type MemoryAidViewProps = {
  /** The associated memory aid sentence. */
  content: string;
};

/**
 * Renders a <MemoryAidView /> component.
 */
const MemoryAidView = (props: MemoryAidViewProps): JSX.Element | null => {
  let content = props.content;
  // let test = props.content;

  if (!content || content === "TODO") return null;

  content = content.replace(
    new RegExp(
      "([\u2E80-\u2FD5\u3190-\u319f\u3400-\u4DBF\u4E00-\u9FCC\uF900-\uFAAD]+)",
      "g"
    ), // matches all brackets enclosing only Chinese chars
    "<span class='use-serifs' style='color: #00838F; font-size: 1.2em'>$1</span>"
    // ).replace(
    //     new RegExp('<(?!span|/)(.*?)>', 'g'), // match inside brackets other than span tags
    //     '<span class=\'use-serifs\' style=\'color: darkcyan\'>$1</span>'
  );

  return (
    <>
      {/* <MemoryAidHeading>
                Memory Aid
            </MemoryAidHeading> */}
      <MemoryAidContent
        style={{ whiteSpace: "pre-line" }}
        dangerouslySetInnerHTML={{ __html: content }}
      />
    </>
  );
};

type Props = {
  /**
   * The word object to be rendered, if not provided,
   * url will be used to construct the object.
   */
  word?: Word;

  /**
   * The URL of the word to be rendered, if it
   * is not provided, then the qid is used to construct
   * the url.
   */
  url?: string;

  /**
   * The query id of the word to be rendered, will
   * be omitted if url is present and not null.
   */
  qid?: number;

  /* Determine whether the breakdown view is always expanded. */
  autoExpandBreakdown?: boolean;
};

/**
 * The main function that renders a word view.
 */
const WordDisplay = (props: Props): JSX.Element => {
  const word: Word | null =
    props.word == null
      ? useLoadWord(
          props.url == null ? `/content/word/${props.qid}` : props.url
        )
      : props.word;

  const renderBreakdown = (word: Word): JSX.Element => {
    // if it is single-character word, the characters field will be a list of
    // a single serialized character, render that character's breakdown view
    if (word.characters.length === 1) {
      const radicals = word.characters[0].split(";");
      return (
        <BreakdownView
          type="radical"
          alwaysDisplay={props.autoExpandBreakdown ?? true}
          componentURL={radicals}
          memoryAid={word.memoryAid}
        />
      );
    } else {
      return (
        <BreakdownView
          type="word"
          alwaysDisplay={props.autoExpandBreakdown ?? true}
          componentURL={word.characters}
          memoryAid={word.memoryAid}
        />
      );
    }
  };

  // type DescriptionProps = {
  //     description : string,
  // }

  // const WordDescription = (wordDescription:DescriptionProps) : JSX.Element => {

  //     const description = wordDescription.description.replace(
  //         new RegExp('<(.*?)>', 'g'),
  //         '<span class=\'use-serifs\' style=\'color: #00838F\'>$1</span>'
  //     )

  //     return (
  //         <div className='use-serifs' dangerouslySetInnerHTML={{__html:description}} />
  //     )
  // }

  const renderWord = (word: Word): JSX.Element => {
    const chinese = word.chinese;
    const pinyin = word.pinyin;
    const definitions = word.definitions;
    const audioURL = word.audioUrl;
    const memoryAid = word.memoryAid;

    return (
      <>
        <ContainerTop>
          <WordDefinition
            audioURL={audioURL}
            chinese={chinese}
            pinyin={pinyin}
            definitions={definitions}
          />
        </ContainerTop>
        <div className="wrap">
          <div className="left">
            <MemoryAidView content={memoryAid} />
            {renderBreakdown(word)}
            <br />
          </div>
          <ContainerRight className="right">
            <ContainerRightTop>
              {word.sentences.map((sen) => {
                return (
                  <ExampleSentences
                    key={sen.chineseHighlight}
                    word={word}
                    pinyin={sen.pinyinHighlight}
                    audioURL={sen.audioUrl}
                    chinese={sen.chineseHighlight}
                    translation={sen.translationHighlight}
                  />
                );
              })}
            </ContainerRightTop>
            <RelatedItems
              items={word.relatedWords}
              item={word.chinese}
              itemType="word"
            />
          </ContainerRight>
        </div>
      </>
    );
  };

  if (word === null) {
    return <LoadingView />;
  } else {
    return renderWord(word);
  }
};

export default WordDisplay;
