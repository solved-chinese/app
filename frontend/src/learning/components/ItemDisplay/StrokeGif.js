// WordContainer is moved to here
// npm install hanzi-writer
import HanziWriter from 'hanzi-writer';
import React, {useEffect, useState} from 'react';
import styled from 'styled-components';
import '@learning.styles/ItemDisplay.css';
import PropTypes from 'prop-types';

const WordContainer = styled.div`
    font-size: 3.75em;
    font-weight: 200;
    text-align: center;
    display: flex;
    flex-direction: column;
`;

/**
 * @param {String} props.item
 * @param {Object} props
 * @returns {JSX.Element}
 * @constructor
 */
export default function StrokeGif(props) {

    console.log(props.item);

    /* Split input into array of characters. */
    const items = props.item.split('');

    /* Create target ID for each of the characters. */
    const itemsTargetIDs = items.map((value, index) => `writer-target-${index}`);

    let writers = null;

    // Wanted to: when clicked, render gif
    // const [gif1, setGif1] = useState(false);
    
    // Should useEffect be called only when clicked?
    // Can it be put into <div onClick=?> 
    // useEffect(() => {
    //
    //     document.getElementById('div-writer1').addEventListener('click', () => {
    //         writer.animateCharacter();
    //     });
    //     // How to hook the three actions -- animate, pause, resume -- in series?
    //     document.getElementById('div-writer1').addEventListener('click', () => {
    //         writer.pauseAnimation();
    //     });
    //
    //     document.getElementById('div-writer1').addEventListener('click', () => {
    //         writer.resumeAnimation();
    //     });
    // }, []);

    /* Instantiate writers after rendering. */
    useEffect(() => {
        writers = itemsTargetIDs.map((value, index) =>
            HanziWriter.create(value, items[index], {
                width: 100,
                height: 100,
                padding: 5,
                showOutline: true,
                showCharacter: true
            })
        );
    }, []);

    const writerOnclick = () => {

    };

    const renderWriterTarget = () => itemsTargetIDs.map(
        (id, index) => (
            <div id={id} key={index} />
        )
    );

    return (
        <div>
            <WordContainer className='use-chinese'>
                {/* Writer Target */}
                {renderWriterTarget()}
            </WordContainer>

        </div>
        
    );
}


StrokeGif.propTypes = {
    item: PropTypes.string,
};
