import React from "react";
import styled from "styled-components";

import RelatedItems from "@learning.components/ItemDisplay/RelatedItems";
import LoadingView from "@learning.components/ItemDisplay/LoadingView";
import useLoadRad from "@learning.hooks/useLoadRad";

import { Radical } from "@interfaces/CoreItem";

import "@learning.styles/ItemDisplay.css";
import RadicalExplanation from "./RadicalExplanation";

const Row = styled.div`
  display: inline-flex;
  min-width: 100%;
  flex-wrap: wrap;
  flex-direction: row;
`;

interface StyledProps {
  withoutExp: boolean;
}

const DefContainer = styled.div<StyledProps>`
  display: flex;
  min-width: 60%;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  margin-bottom: 20px;
  flex-direction: column;
  width: ${(props) => (props.withoutExp ? "auto" : "100%")};
`;

const Column = styled.div`
  display: flex;
  min-width: 100%;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  margin-bottom: 20px;
  flex-direction: column;
  background-color: #fafafa; // off-white
`;

const MnemonicImage = styled.img`
  width: 200px;
  min-width: 35%;
  max-height: 300px;
  max-width : 100%;
  object-fit: contain;
`;

const RadDefinition = styled.i`
  flex-grow: 2;
  font-size: 1.45em;
  text-align: center;
  width: auto;
  min-width: 20px;
  margin-top: 10px;
`;

const Phonetic = styled.div`
  text-align: center;
  font-size: 1.3em;
  font-weight: 200;
  white-space: nowrap;
`;

const SpeakButton = styled.i`
  position: relative;
  margin-left: 10px;
  margin-top: auto;
  font-weight: 200;
  cursor: pointer;
`;

const DefPhoneticContainer = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: center;
`;

const DefPinyinContainer = styled.div`
  display: flex;
  height: 20px;
  flex-direction: column;
  justify-content: center;
`;

const ExpContainer = styled.a<StyledProps>`
  position: relative;
  display: ${(props) => (props.withoutExp ? "flex" : "none")};
  width: 40%;
  justify-items: center;
  align-items: center;
`;

type Props = {
  /**
   * The radical object to be rendered, if not provided,
   * the url param will be used to fetch the object.
   */
  radical?: Radical;

  /**
   * URL of the radical to be rendered, if it
   * is not provided, then the qid is used to construct
   * the url.
   */
  url?: string;

  /**
   * The query id of the radical to be rendered, will
   * be omitted if url is present and not null.
   */
  qid?: number;
};

/**
 * The main function that renders a radical view.
 */
export const RadStandardDisplay = (props: Props): JSX.Element => {
  const radical =
    props.radical == null
      ? useLoadRad(
          props.url == null ? `/content/radical/${props.qid}` : props.url
        )
      : props.radical;

  const audio = radical != null ? new Audio(radical.audioUrl) : null;

  const renderRadical = (radical: Radical) => {
    // const chinese = radical.chinese;
    // const def = radical.definition;
    // const explanation = radical.explanation;
    const imageUrl = radical.image;

    return (
      <>
        <DefPinyinContainer>
          {radical.pinyin !== "" && (
            <Phonetic className="use-chinese">
              {radical.pinyin}
              <SpeakButton
                className="fas fa-volume"
                onClick={() => audio?.play()}
              />
            </Phonetic>
          )}
        </DefPinyinContainer>
        <MnemonicImage src={imageUrl} />
      </>
    );
  };

  if (radical === null) {
    return <LoadingView />;
  } else {
    return renderRadical(radical);
  }
};

/**
 * The main function that renders a radical view.
 */
export const RadDisplayWithSignal = (props: Props): JSX.Element => {
  const radical =
    props.radical == null
      ? useLoadRad(
          props.url == null ? `/content/radical/${props.qid}` : props.url
        )
      : props.radical;

  const renderRadical = (radical: Radical) => {
    const def = radical.definition;
    const explanation = radical.explanation;
    return (
      <>
        <Column>
          <RadStandardDisplay
            radical={props.radical}
            qid={props.qid}
            url={props.url}
          />
          <DefPhoneticContainer>
            <RadDefinition className="use-serifs">{def}</RadDefinition>
            <RadicalExplanation explanation={explanation} />
          </DefPhoneticContainer>
        </Column>
      </>
    );
  };

  if (radical === null) {
    return <LoadingView />;
  } else {
    return renderRadical(radical);
  }
};

/**
 * The main function that renders a radical view.
 */
const RadDisplay = (props: Props): JSX.Element => {
  const radical =
    props.radical == null
      ? useLoadRad(
          props.url == null ? `/content/radical/${props.qid}` : props.url
        )
      : props.radical;

  const renderRadical = (radical: Radical) => {
    // const chinese = radical.chinese;
    const def = radical.definition;
    const explanation = radical.explanation;

    return (
      <Row>
        <DefContainer withoutExp={explanation !== ""}>
          <RadStandardDisplay
            radical={props.radical}
            qid={props.qid}
            url={props.url}
          />
          <RadDefinition className="use-serifs">{def}</RadDefinition>
        </DefContainer>
        <ExpContainer withoutExp={explanation !== ""}>
          {explanation}
        </ExpContainer>
      </Row>
    );
  };

  if (radical === null) {
    return <LoadingView />;
  } else {
    return renderRadical(radical);
  }
};

export default RadDisplay;

type RadImageProps = {
  /** Url of the radical image */
  url: string;

  /**
   * The text radical to be displayed, in case
   * of an error.
   */
  radical: string;
};

type RadImageState = {
  errored: boolean;
};

export class RadImage extends React.Component<RadImageProps, RadImageState> {
  constructor(props: RadImageProps) {
    super(props);
    this.state = {
      errored: false,
    };
  }

  /**
   * Callback function when there's an error loading
   * the img tag.
   */
  onError = (): void => {
    this.setState({ errored: true });
  };

  render(): JSX.Element {
    const { radical, url } = this.props;
    return this.state.errored ? (
      <>radical</>
    ) : (
      <img src={url} alt={radical} onError={this.onError} />
    );
  }
}
