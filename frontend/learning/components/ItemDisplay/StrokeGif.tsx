import HanziWriter from "hanzi-writer";
import React from "react";
import styled from "styled-components";
import "@learning.styles/ItemDisplay.css";
import { makeID } from "@utils/utils";


export const width = 200;
export const height = 200;

export const WordContainer = styled.div`
  display: flex;
  flex-direction: row;
  text-align: center;
  width: 100%;
  justify-content: center;
  align-items: center;
`;

export const CharSVGContainer = styled.div`
  font-size: 2.75em;
  width: 100%;
  font-weight: 200;
  text-align: center;
  justify-content: center;
  aligh-items: center;
  color: var(--primary-text);
`;




// Enumeration for states
enum WriterState {
  STANDBY = "standby",
  PLAYING = "playing",
  PAUSED = "paused",
  LOOPING = "looping",
}

type StrokeGifProps = {
  item: string;
};

/**
 * Render characters with HanziWriter, allowing clicking for
 * stroke order animations.
 */
export default class StrokeGif extends React.Component<StrokeGifProps> {
  private writers: HanziWriter[] = [];
  private writerStates: WriterState[] = [];
  private itemsTargetIDs: string[] = [];
  private items: string[] = [];
  private itemsTargetRef: React.RefObject<HTMLDivElement>[] = [];

  constructor(props: StrokeGifProps) {
    super(props);
  }

  componentDidMount(): void {
    this.writers = this.getWriters(this.itemsTargetIDs, this.items);
    this.writerStates = this.getInitialWriterStates(this.items.length);
  }

  componentDidUpdate(): void {
    this.writers = this.getWriters(this.itemsTargetIDs, this.items);
    this.writerStates = this.getInitialWriterStates(this.items.length);
  }

  getWriters(targetIDs: string[], items: string[]): HanziWriter[] {
    return targetIDs.map((value, index) =>
      HanziWriter.create(value, items[index], {
        width: width, // defined on the top
        height: height,
        padding: 2,
        strokeAnimationSpeed: 1, // times the normal speed
        delayBetweenStrokes: 5, // ms between strokes
        showOutline: true,
        showCharacter: true,
        strokeColor: "#303545",
        delayBetweenLoops: 500,
        onLoadCharDataError: () => {
          if (this.itemsTargetRef[index].current) {
            this.itemsTargetRef[index].current!.innerText = items[index];
          }
        },
      })
    );
  }

  getInitialWriterStates(n: number): WriterState[] {
    const arr = [];
    for (let i = 0; i < n; i++) {
      arr.push(WriterState.LOOPING);
    }
    return arr;
  }

  renderWriterTarget(): JSX.Element[] {
    return this.itemsTargetIDs.map((id, index) => (
      <CharSVGContainer
        id={id}
        key={this.itemsTargetIDs[index]}
        style={{ cursor: "grab" }}
        onLoadCapture={() => this.writerCallback(index)}
        onClick={() => this.writerCallback(index)}
        className="use-chinese"
        ref={this.itemsTargetRef[index]}
      />
    ));
  }

  writerCallback(index: number): void {
    const writer = this.writers[index];
    switch (this.writerStates[index]) {
      case WriterState.STANDBY:
        writer
          .animateCharacter({
            onComplete: () => {
              this.writerStates[index] = WriterState.STANDBY;
            },
          })
          .then(() => {
            this.writerStates[index] = WriterState.PLAYING;
          });
        break;
      case WriterState.PLAYING:
        writer.pauseAnimation().then(() => {
          this.writerStates[index] = WriterState.PAUSED;
        });
        break;
      case WriterState.PAUSED:
        writer.resumeAnimation().then(() => {
          this.writerStates[index] = WriterState.PLAYING;
        });
        break;
      case WriterState.LOOPING:
        writer.loopCharacterAnimation();
        break;
    }
  }

  render(): JSX.Element[] {
    this.items = this.props.item.split("");
    this.itemsTargetIDs = this.items.map(
      (value, index) => `writer-target-${index}-${makeID(5)}`
    );
    this.itemsTargetRef = this.itemsTargetIDs.map(() => React.createRef());

    /* the key is id here */
    const writerTargets = this.renderWriterTarget().map( (target, id) => {
      return <WordContainer key={id}> 
        {target}
      </WordContainer>
    });
    return writerTargets
  }
}
