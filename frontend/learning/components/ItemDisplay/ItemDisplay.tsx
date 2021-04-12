import React from 'react';

import CharDisplay from './CharacterDisplay/CharDisplay';
import WordDisplay from './WordDisplay/WordDisplay';
import RadDisplay from './RadicalDisplay/RadDisplay';

import '@learning.styles/ItemDisplay.css';

import {ItemType} from '@interfaces/CoreItem';
import styled from 'styled-components';

const NextButton = styled.button`
    display: block;
    border: 1px solid var(--main-theme-color);
    color: var(--main-theme-color);
    background-color: white;
    padding: 0.4em 2em;
    margin-top: -35px;
    text-align: right;
    transition: all 150ms ease-in-out;
    border-radius: 3px;
    font-size: 0.9em;
  
    &:hover {
        background-color: var(--main-theme-color);
        color: white;
    }
`;

type Props = {
    type?: ItemType,
    qid: number,
    hasNext?: boolean,
    onActionNext?: ()=>void,
    displayRef?: React.RefObject<HTMLDivElement>
}

/**
 * Statically display an item (word, character, or radical) 
 * using an ItemDescriptor.
 */
const ItemDisplay = (props: Props): JSX.Element => {
    
    const renderSwitch = (type: ItemType | undefined, qid: number) => {
        switch (type) {
        case 'character':
            return (<CharDisplay qid={qid} />);
        case 'radical':
            return <RadDisplay qid={qid} />;
        case 'word':
            return <WordDisplay qid={qid} />;
        default:
            return ; // TODO: Error handling
        }
    };

    const renderNext = () => {
        if (props.onActionNext !== undefined) {
            const onActionNext = props.onActionNext;
            return (
                <div>
                    <NextButton onClick={() => onActionNext() }>
                        Next
                    </NextButton>
                </div>
            );
        }
    };

    return (
        <>
            <div className='content-card-container box-shadow'
                ref={props.displayRef} tabIndex={0} style={{outline: 'none'}}
            >
                { renderSwitch(props.type!, props.qid) }
            </div>
            { renderNext() }
        </>
    );
};

export default ItemDisplay;