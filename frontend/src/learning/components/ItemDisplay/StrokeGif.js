// WordContainer is moved to here
// npm install hanzi-writer
import HanziWriter from 'hanzi-writer';
import React, {useEffect, useState} from 'react';
import styled from 'styled-components';
import '@learning.styles/ItemDisplay.css';
import PropTypes, { any } from 'prop-types';

const WordContainer = styled.h1`
    font-size: 3.75em;
    font-weight: 200;
    text-align: center;
    display: flex;
    flex-direction: column;
`;



export default function StrokeGif(props) {

    // Wanted to change into props but got error?
    // const char1 = props.item.substring(0,1)
    const char1 = '你';
    const char2 = '好';

    // Wanted to: when clicked, render gif
    const [gif1, setGif1] = useState(false);
    
    // Should useEffect be called only when clicked?
    // Can it be put into <div onClick=?> 
    useEffect(() => {
        var writer = HanziWriter.create('div-writer1', char1, {
            width: 100,
            height: 100,
            padding: 5,
            showOutline: true
        });
        document.getElementById('div-writer1').addEventListener('click', function() {
            writer.animateCharacter();
        });
        // How to hook the three actions -- animate, pasue, resume -- in series?
        document.getElementById('div-writer1').addEventListener('click', function() {
          writer.pauseAnimation();

        document.getElementById('div-writer1').addEventListener('click', function() {
            writer.resumeAnimation();
      });
    }, []);

    console.log(gif1);

    return (
        <div>
            <WordContainer className='use-chinese'>                
                <div onClick={() => 
                    useEffect(() => {
                        var writer = HanziWriter.create('div-writer1', char1, {
                            width: 100,
                            height: 100,
                            padding: 5,
                            showOutline: true
                        });
                        document.getElementById('div-writer1').addEventListener('click', function() {
                            writer.animateCharacter();
                        });
                    }, [])}>
                    {char1}</div>
                
                {/* needs to style the same size */}
                <div id='div-writer1'></div>
                
                
                
            </WordContainer>
            
        </div>
        
    );
}


StrokeGif.propTypes = {
    item: PropTypes.string,
};
