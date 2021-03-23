import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import '@learning.styles/ItemDisplay.css';
import ItemPhonetic from '@learning.components/ItemDisplay/ItemPhonetic';

const TableContainer = styled.table`
    margin-left: 70px;
    font-size: 1.3em;
    max-width: 500px;

    @media only screen and (max-width: 480px) {
        padding: 0;
    }
`;

const PofSpeech = styled.td`
    font-style: italic;
    text-align: left;
`;

const ListTitle = styled.th`
    font-size: 0.7em;
    font-style: normal;
    color: var(--teritary-text);
    font-weight: 400;
    line-height: 1em;
`;

function Definitions(props) {

    const definitions = props.definitions.map(d => {
        return (
            <tr key={d.definition}>
                <PofSpeech className='use-serifs'>
                    {d.partOfSpeech}
                </PofSpeech>
                <td className='use-serifs'>
                    {d.definition}
                </td>
            </tr>
        );
    });

    return (
        <TableContainer>
            <tbody>
                <tr>
                    <ListTitle>Definitions</ListTitle>
                </tr>
                {definitions}
            </tbody>
        </TableContainer>
    );
}

Definitions.propTypes = {
    definitions: PropTypes.any
};

export default function WordDefinition(props) {

    console.log(props.audioURL);
    return (
        <>
            <ItemPhonetic
                item={props.chinese}
                pinyin={props.pinyin}
                audioURL={props.audioURL}
                useStroke={true}
            />
            <Definitions
                definitions={props.definitions}
            />
        </>
    );
}

WordDefinition.propTypes = {
    /** The word in chinese */
    chinese: PropTypes.string.isRequired,

    /** Resource URL of the audio pronunciation */
    audioURL: PropTypes.string.isRequired,

    /** Pronunciation in pinyin */
    pinyin: PropTypes.string.isRequired,

    /** A list of definitions associated with the word.
     * A definition object contains two entries: the
     * definition string and its part of speech.
     */
    definitions: PropTypes.arrayOf(
        PropTypes.shape({
            part_of_speech: PropTypes.string,
            definition: PropTypes.string
        })
    ),
};
