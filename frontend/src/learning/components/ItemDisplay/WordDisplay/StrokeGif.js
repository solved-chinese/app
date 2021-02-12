
// npm install hanzi-writer
// StrokeGif now moved to "/ItemDisplay/WordDisplay"
import HanziWriter from 'hanzi-writer';
import React, {useEffect, useState} from 'react';
import styled from 'styled-components';
import '@learning.styles/ItemDisplay.css';
import PropTypes from 'prop-types';

const WordContainer = styled.div`
    font-size: 3.75 em;
    font-weight: 200;
    text-align: center;
    display: flex;
    flex-direction: row;
`;

/**
 * @param {String} props.item
 * @param {Object} props
 * @returns {JSX.Element}
 * @constructor
 */
export default function StrokeGif(props) {

    /* Split input into array of characters. */
    const items = props.item.split('');

    /* Create target ID for each of the characters. */
    const itemsTargetIDs = items.map((value, index) => `writer-target-${index}`);

    let writers = null;

    // Might need write two states?
    //     gifState1 and gifState2
    const [gifState, setGifState] = useState(-2);

    // new useEffect that switches between three aminations:
    //     gifState === -2  -> create writer
    //     gifState === -1  -> animateCharacter()
    //     gifState % 2 === 0  -> pauseAnimation()
    //     gifState % 2 === 1  -> resumeAnimation()
    useEffect(() => {
        // initial state is -2
        if(gifState === -2){
            writers = itemsTargetIDs.map((value, index) =>
                HanziWriter.create(value, items[index], {
                    width: 60,
                    height: 65,
                    padding: 2,
                    showOutline: true,
                    showCharacter: true,
                })
            );            
        }
        // first click start -> state = -1
        if(gifState === -1){
            // writers.animateCharacter();

            //document.getElementById('writer-target-1').addEventListener('click', () => {
            //  writers.animateCharacter();});
            console.log('clicked createAnimation');
        }
        // second click pause -> state = 0
        if(gifState >= 0 && gifState % 2 === 0){
            //writers.animateCharacter();

            //document.getElementById('writer-target-1').addEventListener('click', () => {
            //  writers.pauseCharacter();});
            console.log('clicked pauseAnimation');
        }
        // third click resume -> state = 1
        if(gifState >= 0 && gifState % 2 === 1){
            // writers.resumeCharacter();

            //document.getElementById('writer-target-1').addEventListener('click', () => {
            //  writers.resumeCharacter();});
            console.log('clicked resumeAnimation');
        }

    }, [gifState]);

    // added 'onClick' to <div>
    const renderWriterTarget = () => itemsTargetIDs.map(
        (id, index) => (
            <div id={id} key={index} style={{cursor: 'grab'}} onClick={() => writerOnclick(index)}/>
        )
    );
    
    // gifState adds one when clicked
    const writerOnclick = (index) => {
        setGifState(gifState +1); // How to write into ' gifState${index} ' ?
        console.log('gifState is ' + gifState);
        console.log('index is ' + index);
    };


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
