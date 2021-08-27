import React from "react";
import styled from "styled-components";
import "@learning.styles/ItemDisplay.css";
import ItemPhonetic from "@learning.components/ItemDisplay/ItemPhonetic";
import { ItemDefinition } from "@interfaces/CoreItem";

const TableContainer = styled.table`
  margin-left: 70px;
  font-size: 1.3em;
  max-width: 500px;

  @media only screen and (max-width: 480px) {
    padding: 0;
  }
`;

const PofSpeech = styled.td`
  font-style: italic;
  text-align: left;
`;

const ListTitle = styled.th`
  font-size: 0.7em;
  font-style: normal;
  color: var(--teritary-text);
  font-weight: 400;
  line-height: 1em;
`;

type DefinitionsProps = {
  definitions: ItemDefinition[];
};

const Definitions = (props: DefinitionsProps): JSX.Element => {
  const definitions = props.definitions.map((d, index) => {
    return (
      <tr key={index}>
        <PofSpeech className="use-serifs">{d.partOfSpeech}</PofSpeech>
        <td className="use-serifs">{d.definition}</td>
      </tr>
    );
  });

  return (
    <TableContainer>
      <tbody>
        <tr>
          <ListTitle>Definitions</ListTitle>
        </tr>
        {definitions}
      </tbody>
    </TableContainer>
  );
};

type WordDefinitionProps = {
  /** The word in chinese */
  chinese: string;

  /** Resource URL of the audio pronunciation */
  audioURL: string;

  /** Pronunciation in pinyin */
  pinyin: string;

  /**
   * A list of definitions associated with the word.
   * A definition object contains two entries: the
   * definition string and its part of speech.
   */
  definitions: ItemDefinition[];
};
const WordDefinition = (props: WordDefinitionProps): JSX.Element => {
  return (
    <>
      <ItemPhonetic
        item={props.chinese}
        pinyin={props.pinyin}
        audioURL={props.audioURL}
        useStroke={true}
      />
      <Definitions definitions={props.definitions} />
    </>
  );
};

export default WordDefinition;
