
import HanziWriter from 'hanzi-writer';
import React, {useEffect, useState} from 'react';
import styled from 'styled-components';
import '@learning.styles/ItemDisplay.css';
import PropTypes from 'prop-types';
import {makeid} from '../../../utils/utils';

const WordContainer = styled.div`
    font-size: 3.75em;
    font-weight: 200;
    text-align: center;
    display: flex;
    flex-direction: row;
`;

/**
 * Render characters with HanziWriter, allowing clicking for
 * stroke order animations.
 * @param {String} props.item
 * @param {Object} props
 * @returns {JSX.Element}
 */
export default function StrokeGif(props) {

    /* Split input into array of characters. */
    const items = props.item.split('');

    /* Create target ID for each of the characters. */
    const itemsTargetIDs = items.map((value, index) =>
        `writer-target-${index}-${makeid(5)}`);

    // an array of 'writers'
    const writers = itemsTargetIDs.map(() => useState(null));

    // Enumeration for states
    const GifState = {
        STANDBY: 'standby',
        PLAYING: 'playing',
        PAUSED: 'paused'
    };

    const gifStatesBundle = itemsTargetIDs.map(() => useState(GifState.STANDBY));

    useEffect(() => {
        // Initialize the writers into state
        itemsTargetIDs.forEach((value, index) => {
            const [, setWriter] = writers[index];
            setWriter(HanziWriter.create(value, items[index], {
                width: 60,
                height: 65,
                padding: 2,
                showOutline: true,
                showCharacter: true,
            }));
        });
    },[]); 

    const renderWriterTarget = () => itemsTargetIDs.map(
        (id, index) => (
            <div
                id={id} key={index} style={{cursor: 'grab'}}
                onClick={() => writerCallback(index)}
            />
        )
    );

    // Handle the character click
    const writerCallback = (index) => {
        const [gifState, setGifState] = gifStatesBundle[index];
        const [writer, ] = writers[index];
        switch (gifState) {
        case GifState.STANDBY:
            writer.animateCharacter({
                onComplete: () => {
                    setGifState(GifState.STANDBY);
                }
            });
            setGifState(GifState.PLAYING);
            break;
        case GifState.PLAYING:
            writer.pauseAnimation();
            setGifState(GifState.PAUSED);
            break;
        case GifState.PAUSED:
            writer.resumeAnimation();
            setGifState(GifState.PLAYING);
            break;
        }
    };

    return (
        <div>
            <WordContainer className='use-chinese'>
                {/* How render div only once? */}
                {renderWriterTarget()}
            </WordContainer>
        </div>
    );
}

StrokeGif.propTypes = {
    item: PropTypes.string,
};
