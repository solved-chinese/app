import React from 'react';
import styled from 'styled-components';
import PropTypes from 'prop-types';

const Heading = styled.h2`
    color: ${props => props.theme.teritaryText};
    font-size: 0.8em;
    font-weight: 400;
`;

const RelatedWordsList = styled.ul`
    line-height: 1.5em;
`;

/** Display related words that a user has seen. */
export default class RelatedWords extends React.Component {

    static propTypes = {
        /** The character used to look up related */
        character: PropTypes.string.isRequired
    }

    constructor(props) {
        super(props);
        this.words = [
            {
                word: '学生',
                phonetic: 'xuéshēng',
                def: 'n. student'
            },
            {
                word: '学校',
                phonetic: 'xuéxiào',
                def: 'n. school'
            }
        ];
    }

    render() {
        return (
            <>
                <Heading>
                    Related words you&apos;ve seen
                </Heading>
                <RelatedWordsList>
                    {this.words.map((v, i) => {
                        return (<RelatedWordItem 
                            style={ i % 2 ? {background : '#F9F9F9'} : {}}
                            key={v.word} 
                            word={v}
                        />);
                    })}
                </RelatedWordsList>
            </>
        );
    }
}

const RelatedWordItemDisplay = styled.li`
    display: flex;
    justify-content: flex-start;
    padding: 3px 3px 3px 6px;
`;

const ItemComp = styled.p`
    display: inline-block;
    font-size: 1em;
    color: ${ props => props.theme.secondaryText };
    padding-right: 20px;
    margin-bottom: 0;
`;

const ItemCompWord = styled(ItemComp)`
    font-size: 1.2em;
`;

const ItemCompPhonetic = styled(ItemComp)`
    font-size: 0.9em;
    flex-grow: 2;
`;

const ItemCompDef = styled(ItemComp)`
    width: 60%;
`;
class RelatedWordItem extends React.Component {

    static propTypes = {
        word: PropTypes.object,
        style: PropTypes.object
    }

    render() {
        const {word, phonetic, def} = this.props.word;

        // TODO: The curly 
        return (
            <RelatedWordItemDisplay style={this.props.style} >
                <ItemCompWord className='use-serifs'>
                    {word}
                </ItemCompWord>
                <ItemCompPhonetic className='use-serifs'>
                    {`/${phonetic}/`}
                </ItemCompPhonetic>
                <ItemCompDef className='use-serifs'>
                    {def}
                </ItemCompDef>
            </RelatedWordItemDisplay>
        );
    }
}