import React from 'react';
import styled from 'styled-components';

import RelatedItems from './RelatedItems';
import ItemPhonetic from './ItemPhonetic';

import useLoadRad from '@learning.hooks/useLoadRad';
import useLoadChar from '@learning.hooks/useLoadChar';

import ItemDisplayPopup from './ItemDisplayPopup';

import '@learning.styles/ItemDisplay.css';
import {Character, Radical} from '@interfaces/CoreItem';

const Row = styled.div`
    display: inline-flex;
    min-width: 100%;
    justify-content: space-evenly;
    align-items: center;
    flex-wrap: nowrap;
    margin-bottom: 20px;

    @media only screen and (max-width: 480px) {
        flex-wrap: wrap;
    }
`;

const MnemonicImage = styled.img`
    width: 35%;
    min-width: 150px;
    max-height: 300px;
    object-fit: contain;
`;

const RadDefinition = styled.h4`
    display: inline-block;
    width: 100%;
    font-size: 1.3em;
    text-align: center;
    min-width: 60px;
    margin-top: 15px;
`;

const Phonetic = styled.span`
    text-align: center;
    font-size: 1.6em;
    font-weight: 200;
    white-space: nowrap;
`;

const SpeakButton = styled.i`
    position: relative;
    margin-left: 10px;
    margin-top: auto;
    font-weight: 200;
    cursor: pointer;
`;

const DefPhoneticContainer = styled.div`
    display: inline-flex;
    flex-direction: column;
    justify-content: center;
`;

const Explanation = styled.div`
    color: var(--secondary-text);
    font-size: 0.8em;
    text-align: center;
`;

type BreakdownRadProps = {
    url: string
}

/** 
 * Render a single character breakdown display using the
 * radical in props.url. Re-render automatically when props.url
 * updates to a new value.
 */
const BreakdownRad = (props: BreakdownRadProps): JSX.Element => {

    const radical = useLoadRad(props.url);

    const renderRadical = (radical: Radical) => {
        const chinese = radical.chinese;
        const def = radical.definition;
        const imageUrl = radical.image;
        const explanation = radical.explanation;
        const audio = new Audio(radical.audioUrl);

        return (
            <>
                <Row>
                    <MnemonicImage src={imageUrl}/>
                    <DefPhoneticContainer>
                        { radical.pinyin !== '' && (
                            <Phonetic className='use-chinese'>
                                { radical.pinyin }
                                <SpeakButton
                                    className='fas fa-volume'
                                    onClick={() => audio.play()}
                                />
                            </Phonetic>
                        )}
                        <RadDefinition className='use-serifs'>
                            {def}
                        </RadDefinition>
                    </DefPhoneticContainer>
                </Row>
                {
                    explanation !== '' && (
                        <Row>
                            <Explanation>
                                {explanation}
                            </Explanation>
                        </Row>
                    )
                }
                <RelatedItems
                    item={chinese}
                    items={radical.relatedCharacters}
                    itemType='character' />
            </>
        );
    };

    if (radical === null) {
        return React.createElement('Loading character data');
    } else {
        return renderRadical(radical);
    }
};

const CharDefList = styled.ul`

    padding-left: 10px;
    font-size: 1.3em;

    @media only screen and (max-width: 480px) {
        padding: 0;
    }
`;

const CharDefListItem = styled.li`
    line-height: 1.75em;
`;

type BreakdownCharProps = {
    url: string
}

/** 
 * Render a single word breakdown display using the
 * character in props.url. Re-render automatically 
 * when props.url updates to a new value.
 */
const BreakdownChar = (props: BreakdownCharProps): JSX.Element => {

    const character = useLoadChar(props.url);

    const renderDefinitions = (definitions: string[]) => {
        return (
            <CharDefList>
                { definitions.map( (elem, i) => {
                    return (
                        <CharDefListItem 
                            key={i}
                            className='use-serifs'
                        >
                            · {elem}
                        </CharDefListItem>
                    );
                })}
            </CharDefList>
        );
    };

    const renderCharacter = (character: Character) => {
        const definitions = character.definitions.map( v => 
            v.definition
        );
        return (
            <>
                {/* This should be optimized (character is
                    loaded twice) */}
                <ItemDisplayPopup
                    contentURL = {props.url}
                    type = 'character'
                />

                <Row>
                    <ItemPhonetic pinyin={character.pinyin}
                        audioURL={character.audioUrl}
                        item={character.chinese}
                    />
                    {renderDefinitions(definitions)}
                </Row>
                {/* Added items (related_words) as a props */}
                {/*<RelatedItems */}
                {/*    items={character.relatedWords}*/}
                {/*    item={character.chinese}*/}
                {/*    itemType='word' */}
                {/*/>*/}
            </>
        );
    };

    if (character === null) {
        return React.createElement('Loading character data');
    } else {
        return renderCharacter(character);
    }
};

const MemoryAidHeading = styled.h2`
    display: inline-block;
    width: 100%;
    color: #BEC0C4;
    letter-spacing: 0.6px;
    font-size: 0.9em;
    font-weight: 500;
    text-align: center;
    margin: 20px auto 10px;
`;

const MemoryAidContent = styled.div`
    width: 100%;
    font-size: 0.9em;
    color: var(--secondary-text);
    border-radius: 5px;
    padding: 15px 20px;
    font-weight: 400;
`;

type MemoryAidViewProps = {
    /** The associated memory aid sentence. */
    content: string
}

/**
 * Renders a <MemoryAidView /> component.
 */
const MemoryAidView = (props: MemoryAidViewProps): JSX.Element | null => {

    let content = props.content;

    if (!content || content === 'TODO') return null;

    content = content.replace(
        new RegExp('<([\u2E80-\u2FD5\u3190-\u319f\u3400-\u4DBF\u4E00-\u9FCC\uF900-\uFAAD]+)>',
            'g'), // matches all brackets enclosing only Chinese chars
        '<span class=\'use-serifs\' style=\'color:darkcyan; font-size: 1.2em\'>$1</span>'
    ).replace(
        new RegExp('<(?!span|/)(.*?)>', 'g'), // match inside brackets other than span tags
        '<span class=\'use-serifs\' style=\'color:darkcyan\'>$1</span>'
    );

    return (
        <>
            <MemoryAidHeading>
                Memory Aid
            </MemoryAidHeading>
            <MemoryAidContent
                className='box-shadow'
                style={{whiteSpace: 'pre-line'}}
                dangerouslySetInnerHTML={{__html: content}}
            />
        </>
    );
};

type BreakdownViewProps = {
    /** The type of breakdown components. */
    type: 'radical' | 'word',

    /** URLs of the breakdown components. */
    componentURL: string[],

    /** The associated memory aid sentence. */
    memoryAid: string,

    /** Whether the breakdown view is always expanded. */
    alwaysDisplay: boolean
}

type BreakdownViewState = {
    show: boolean
}

/** Renders a breakdown view for a word or character */
export default class BreakdownView extends React.Component<BreakdownViewProps, BreakdownViewState> {

    constructor(props: BreakdownViewProps) {
        super(props);
        this.state = {
            show: this.props.alwaysDisplay
        };
    }
    

    /**
     * Render the character breakdown for each radical 
     * specified in the urls.
     */
    renderBreakdownRad(urls: string[]) {
        // It is possible to have two breakdown items with the
        // same content (and url), and therefore we cannot use
        // urls as the keys.
        return urls.map( (url, i) => 
            (
                <div key={i}
                    className='breakdown-card box-shadow'>
                    <BreakdownRad url={url} />
                </div>
            )
        );
    }

    /**
     * Render the word breakdown for each character 
     * specified in the urls.
     */
    renderBreakdownChar(urls: string[]) {
        // It is possible to have two breakdown items with the
        // same content (and url), and therefore we cannot use
        // url as the key.
        return urls.map( (url, i) => 
            (
                <div key={i}
                    className='breakdown-card box-shadow'>
                    <BreakdownChar url={url} />
                </div>
            )
        );
    }

    toggle = () => {
        this.setState( prev => ({show: !prev.show}));
    }

    render() {
        const type = this.props.type;
        const toggleTitle = type + ' breakdown';
        const urls = this.props.componentURL;

        return (
            <div className='breakdown-container'>
                <div style={this.props.alwaysDisplay ? {display: 'none'} : {}}
                    className={'breakdown-toggle ' + (
                        this.state.show ? 'toggled' : ''
                    )}
                    onClick={this.toggle}>
                    <h4>
                        {(this.state.show ? 'Close ' : 'Show me the ') +
                            toggleTitle
                        }
                    </h4>
                    <i className={
                        'fas fa-chevron-down ' + 
                        (this.state.show ? 'inversed' : '')} >
                    </i>
                </div>
                <div 
                    className={'breakdown-content ' + (
                        this.state.show ? 'show' : ''
                    )} >

                    { type === 'radical' ?
                        this.renderBreakdownRad(urls) :
                        this.renderBreakdownChar(urls)
                    } 

                    <MemoryAidView
                        content={this.props.memoryAid}/>
                </div>
            </div>
        );
    }
}

