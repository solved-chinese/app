import React from 'react';
import CharItemPhonetic from './CharItemPhonetic.js';
import CharDefinition from './CharDefinition.js';
import styled from 'styled-components';

const Row = styled.div`
    display: flex;
    justify-content: center;
    align-items: center;
    @media only screen and (max-width: 768px) {
        flex-direction: column;
    }
`;

export default class CharDisplay extends React.Component {
    render() {
        return (
            <div className='content-card-container'>
                <Row>
                    <CharItemPhonetic pinyin={['xue']}
                        audioURL=''
                        character='学'/>
                    <CharDefinition 
                        definitions={[
                            'Foo definition',
                            'Bar definition'
                        ]}
                    />
                </Row>
            </div>
        );
    }
}