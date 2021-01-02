import React from 'react'

const ExampleSentences = () => {
  const topText = '/wo shi yi wei xue sheng/'
  const middleText = '我是一位学生'
  const bottomText = 'I am a student'
  return (
    <div className='exampleCard'>
      <p className='topText'>{topText}</p>
      <p className='middleText'>{middleText}</p>
      <p className='bottomText'>{bottomText}</p>
    </div>
  )
}

export default ExampleSentences;