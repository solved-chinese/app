import React from "react";
import styled from "styled-components";
import "@learning.styles/ItemDisplay.css";
import ItemPhonetic from "@learning.components/ItemDisplay/ItemPhonetic";
import { ItemDefinition } from "@interfaces/CoreItem";

const ContainerDefinition = styled.div`
  display: flex;
  justify-content: start;
  align-items: center;
  @media only screen and (max-width: 800px) {
    flex-direction: column;
  }
`;

const TableContainer = styled.div`
  margin-left: 30px;
  font-size: 1.5em;
  width: 100%;
  max-width: 200px;
`;

const PofSpeech = styled.td`
  font-style: italic;
  text-align: left;
  padding-right: 10px;
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
        <PofSpeech className="use-serifs">{d.partOfSpeech}.</PofSpeech>
        <td className="use-serifs">{d.definition}</td>
      </tr>
    );
  });

  return (
    <TableContainer className="divider">
      {/* <tbody> */}
      {/* <tr>
          <ListTitle>Definitions</ListTitle>
        </tr> */}
      {definitions}
      {/* </tbody> */}
    </TableContainer>
  );
};

// type DescriptionProps = {
//     description : string,
// }

// const Description = (props: DescriptionProps): JSX.Element => {

//     const description = props.description.replace(
//         new RegExp('<(.*?)>', 'g'),
//         '<span class=\'use-serifs\' style=\'color: #00838F\'>$1</span>'
//     )

//     return (
//         <Container>
//             {description}
//         </Container>
//     )
// }

type WordDefinitionProps = {
  /** The word in chinese */
  chinese: string;

  /** Resource URL of the audio pronunciation */
  audioURL: string;

  /** Pronunciation in pinyin */
  pinyin: string;

  // /** Descriptiong of the word */
  // description: string,

  // /** The associated memory aid sentence. */
  // memoryAid: string

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
      <ContainerDefinition>
        <ItemPhonetic
          item={props.chinese}
          pinyin={props.pinyin}
          audioURL={props.audioURL}
          useStroke={true}
          type="word"
        />
        {/* <div className="vl"></div> */}
        <Definitions definitions={props.definitions} />
      </ContainerDefinition>
    </>
  );
};

export default WordDefinition;
