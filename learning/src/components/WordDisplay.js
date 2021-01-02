import React from 'react';
import ExampleSentences from './ExampleSentences';
import styled from 'styled-components';
import CharItemPhonetic from './CharItemPhonetic';
import CharDefinition from './CharDefinition';
import RadBreakdown from './RadBreakdown';
import WordDefinition from './WordDefinition';

//Top and Bottom Containters
const ContainerTop = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  @media (max-width: 768px) {
      flex-direction: column;
    }
`;

const ContainerBottom = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  @media (max-width: 768px) {
    flex-direction: column;
  }
`;

export default class WordDisplay extends React.Component {
    render() {
        return (
            <>
                {/* Top: Word Definition*/}
                <ContainerTop>
                    <WordDefinition 
                        src= {'/audio/path'}
                        word={'新生'}
                        pinyin={'/xue sheng/'}
                        definitions={[{definition: 'student', part_of_speech: 'n.'}]}
                    />
                </ContainerTop>



                {/* Bottom: Example Sentences */}
                <p style={{textAlign: 'center', marginTop: '10px', fontSize: '13px'}}>Example Sentences:</p>
                <ContainerBottom>
                    <ExampleSentences 
                        word={{pinyin:'xue sheng', chinese:'学生', definition: 'student'}}
                        pinyin={'/wo shi yi ming xue sheng/'}
                        chinese={'学生是一名学生。'} 
                        translation={'I am a student.'}
                    />
                    <ExampleSentences 
                        word={{pinyin:'xue sheng', chinese:'学生', definition: 'student'}}
                        pinyin={'/wo shi yi ming xue sheng/'}
                        chinese={'学生是一名学生。'} 
                        translation={'I am a student.'}
                    />
                </ContainerBottom>
        
                {/* Show Breakdown toggle. Borrowed from Michael*/}

                <RadBreakdown />

            </>
        );
    }
}