import React from 'react';
import styled from 'styled-components';
import RelatedItems from './RelatedItems.js';

const Row = styled.div`
    display: inline-flex;
    min-width: 100%;
    justify-content: space-around;
    align-items: center;
    flex-wrap: wrap;
    margin-bottom: 20px;
`;

const MnemonicImage = styled.img`
    width: 35%;
    min-width: 150px;
    max-height: 300px;
    object-fit: contain;
`;

const RadDefinition = styled.h4`
    display: inline-block;
    flex-grow: 2;
    font-size: 1.75em;
    text-align: center;
    min-width: 200px;
    margin-top: 20px;
`;

export default class RadDisplay extends React.Component {
    getRadical() {
        
    }
    render() {
        return (
            <>
                <Row>
                    <MnemonicImage 
                        src='/media/mnemonic_image/R0004.png' />
                    <RadDefinition className='use-serifs'>
                        perhaps a longer definition
                    </RadDefinition>
                </Row>
                <RelatedItems 
                    item='somechar'
                    itemType='character' />
            </>
        );
    }
}