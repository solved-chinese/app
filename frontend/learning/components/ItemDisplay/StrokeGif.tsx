
import HanziWriter from 'hanzi-writer';
import React, {} from 'react';
import styled from 'styled-components';
import '@learning.styles/ItemDisplay.css';
import {makeID} from '@utils/utils';

const WordContainer = styled.div`
    display: flex;
    flex-direction: row;
`;

const CharSVGContainer = styled.div`
    font-size: 3.75em;
    font-weight: 200;
    text-align: center;
    color: var(--primary-text);
`;

// Enumeration for states
enum WriterState {
    STANDBY = 'standby',
    PLAYING = 'playing',
    PAUSED = 'paused'
}

type StrokeGifProps = {
    item: string
}

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
                width: 60,
                height: 65,
                padding: 2,
                showOutline: true,
                showCharacter: true,
                strokeColor: '#303545',
                onLoadCharDataError: () => {
                    if (this.itemsTargetRef[index].current) {
                        this.itemsTargetRef[index].current!.innerText = items[index];
                    }
                }
            })
        );
    }

    getInitialWriterStates(n: number): WriterState[] {
        const arr = [];
        for (let i = 0; i < n; i++) {
            arr.push(WriterState.STANDBY);
        }
        return arr;
    }

    renderWriterTarget(): JSX.Element[] {
        return this.itemsTargetIDs.map(
            (id, index) =>
                <CharSVGContainer
                    id={id} key={this.itemsTargetIDs[index]} style={{cursor: 'grab'}}
                    onClick={() => this.writerCallback(index)}
                    className='use-chinese'
                    ref={this.itemsTargetRef[index]}
                />
        );
    }

    writerCallback(index: number): void {
        const writer = this.writers[index];
        switch (this.writerStates[index]) {
        case WriterState.STANDBY:
            writer.animateCharacter({
                onComplete: () => {
                    this.writerStates[index] = WriterState.STANDBY;
                }
            }).then(() => {
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
        }
    }

    render(): JSX.Element {
        this.items = this.props.item.split('');
        this.itemsTargetIDs = this.items.map((value, index) =>
            `writer-target-${index}-${makeID(5)}`);
        this.itemsTargetRef = this.itemsTargetIDs.map(() => React.createRef() );

        return (
            <WordContainer>
                { this.renderWriterTarget() }
            </WordContainer>
        );
    }
}
