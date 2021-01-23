import React from 'react';
import PropTypes from 'prop-types';

import '@learning.styles/ItemDisplay.css';

function ExampleSentences(props) {

    //Add color to the keyword in sentences
    const pinyin = props.pinyin.replace(
        new RegExp('<(.*?)>', 'g'),
        `<span class='use-serifs' style='color:darkcyan'>$1</span>`
    );
    const chinese = props.chinese.replace(
        new RegExp('<(.*?)>', 'g'),
        `<span class='use-serifs' style='color:darkcyan'>$1</span>`
    );
    const translation = props.translation.replace(
        new RegExp('<(.*?)>', 'g'),
        `<span class='use-serifs' style='color:darkcyan'>$1</span>`
    );

    //Output the sentences with HTML <span>
    return (
        <div className='ExampleCard'>
            <div 
                className='sentence-pinyin use-chinese' 
                dangerouslySetInnerHTML={{__html: pinyin}}
            />
            <div 
                className='sentence-chinese use-chinese'
                dangerouslySetInnerHTML={{__html: chinese}}
            />
            <div 
                className='sentence-translation use-serifs' 
                dangerouslySetInnerHTML={{__html: translation}}
            />
        </div>
    
    );
}

ExampleSentences.propTypes = {
    pinyin: PropTypes.string,
    chinese: PropTypes.string,
    translation: PropTypes.string,

    word: PropTypes.object
};

export default ExampleSentences;