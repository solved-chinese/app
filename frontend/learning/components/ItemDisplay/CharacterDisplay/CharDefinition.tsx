import React from "react";
import styled from "styled-components";

import "@learning.styles/ItemDisplay.css";
import ItemPhonetic from "../ItemPhonetic";

const ContainerDefinition = styled.div`
  display: flex;
  justify-content: start;
  align-items: center;
  max-width: 1000px;
  // @media only screen and (max-width: 800px) {
  //     flex-direction: column;
  // }
`;

const DefinitionList = styled.ul`
  display: inline-block;
  padding-left: 30px;
  font-size: 1.3em;
  overflow: hidden;
`;

// const ListTitle = styled.i`
//   font-size: 0.6em;
//   font-style: normal;
//   color: var(--teritary-text);
//   line-height: 1em;
// `;

const ListItem = styled.li`
  line-height: 1.75em;
  text-overflow: ellipsis;
`;

type Props = {
  /** The character in chinese */
  chinese: string;

  /** Resource URL of the audio pronunciation */
  audioURL: string;

  /** Pronunciation in pinyin */
  pinyin: string;

  /** The definitions to be displayed */
  definitions: string[];
};

const CharDefinition = (props: Props): JSX.Element => {
  return (
    <ContainerDefinition>
      <ItemPhonetic
        item={props.chinese}
        pinyin={props.pinyin}
        audioURL={props.audioURL}
        useStroke={true}
      />

      <DefinitionList className="vl">
        {/* <ListTitle>Definitions:</ListTitle> */}
        {props.definitions.map((elem, i) => {
          return (
            <ListItem key={i} className="use-serifs">
              {elem}
            </ListItem>
          );
        })}
      </DefinitionList>
    </ContainerDefinition>
  );
};

export default CharDefinition;
