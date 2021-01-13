import React from 'react';
import PropTypes from 'prop-types';

function ExampleSentences(props) {

    //Add color to the keyword in sentences
    const pinyin = props.pinyin.replace(
        new RegExp(props.word.pinyin, 'g'),
        `<span class='use-serifs'
            style='color:darkcyan'>${props.word.pinyin}</span>`
    );
    const chinese = props.chinese.replace(
        new RegExp(props.word.chinese, 'g'),
        `<span class='use-serifs'
            style='color:darkcyan'>${props.word.chinese}</span>`);
    const translation = props.translation.replace(
        new RegExp(props.word.definitions[0].definition, 'gi'),
        `<span class='use-serifs'
            style='color:darkcyan'>
            ${props.word.definitions[0].definition}
        </span>`);

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