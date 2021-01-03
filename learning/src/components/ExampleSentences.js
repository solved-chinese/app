import React from 'react';

const ExampleSentences = (props) => {

  //Add color to the keyword in sentences
  const pinyin = props.pinyin.replace(new RegExp(props.word.pinyin, 'g'), `<span style='color:darkcyan'>${props.word.pinyin}</span>`) 
  const chinese = props.chinese.replace(new RegExp(props.word.chinese, 'g'), `<span style='color:darkcyan'>${props.word.chinese}</span>`)
  const translation = props.translation.replace(new RegExp(props.word.definitions[0].definition, 'gi'), `<span style='color:darkcyan'>${props.word.definitions[0].definition}</span>`)

  //Output the sentences with HTML <span>
  return (
    <div className='ExampleCard'>
        <div className='sentence-pinyin' dangerouslySetInnerHTML={{__html: pinyin}}/>
        <div className='sentence-chinese'dangerouslySetInnerHTML={{__html: chinese}}/>
        <div className='sentence-translation' dangerouslySetInnerHTML={{__html: translation}}/>
    </div>
    
  )
}

export default ExampleSentences