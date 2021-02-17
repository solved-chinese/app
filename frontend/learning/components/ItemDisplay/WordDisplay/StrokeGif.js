
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

    // an array of 'writers'
    let writers = null; 

    const [gifState1, setGifState1] = useState(0);
    const [gifState2, setGifState2] = useState(0);
    /* 1 - Minor Problem: How to create an array of states?
    const [state, setState] = itemsTargetIDs.map((value, index) => {
        [state[index], setState[index]] = useState(0);
    }); 
    */
    
    /* 2 - Main Problem: after initial useEffect, 'writers' object falls back to 'null';
            When tired to pauseAnimation (didUpdate), 'writers' cannot be referred to.
            Tried passing in a second parameter to induce didUpdate, but triggered re-rendering.
            Thought of cleanup within useEffect, but could not get it working.
    */

    useEffect(() => {

        writers = itemsTargetIDs.map((value, index) => 
            HanziWriter.create(value, items[index], {
                width: 60,
                height: 65,
                padding: 2,
                showOutline: true,
                showCharacter: true,
            })
        );

        function handleChange(){
        }
        return function cleanup(){
        };
    },[]); 

    const renderWriterTarget = () => itemsTargetIDs.map(
        (id, index) => (
            <div id={id} key={index} style={{cursor: 'grab'}} onClick={() => writerCallback(index)}/>
        )
    );
    
    // 3 - Minor Problem: writerCallback seems to animate two characters together?
    // const writerCallback = () => itemsTargetIDs.map(
    //     (_, index) => {
    //         if (gifState1 === 0)
    //             writers[index].animateCharacter();
    //         if (gifState1 % 2 === 1)
    //             writers[index].pauseAnimation();
    //         if (gifState1 % 2 === 0)
    //             writers[index].resumeAnimation();
    //         setGifState1(gifState1 + 1);
    //     }
    // ); 
    
    // Half-fix  Passes in the index and determines which state to change 
    const writerCallback = (index) => {
        // if clicked on gifState 1
        if (index === 0){ 
            if (gifState1 === 0)
                writers[index].animateCharacter();
            if (gifState1 % 2 === 1)
                writers[index].pauseAnimation();
            else
                writers[index].resumeAnimation();

            setGifState1(gifState1 + 1);
        }
        // if clicked on gifState 2
        if (index === 1){
            if (gifState2 === 0)
                writers[index].animateCharacter();
            if (gifState2 % 2 === 1)
                writers[index].pauseAnimation();
            else
                writers[index].resumeAnimation();

            setGifState1(gifState2 + 1);
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
