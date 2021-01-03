import React from 'react';
import 'core-js/stable';
import 'regenerator-runtime/runtime';
import PropTypes from 'prop-types';
import styled from 'styled-components';

import CharItemPhonetic from './CharItemPhonetic.js';
import CharDefinition from './CharDefinition.js';
import RelatedItems from './RelatedItems.js';
import BreakdownView from './BreakdownView';

import LoadingView from './LoadingView.js';


const Row = styled.div`
    display: flex;
    justify-content: center;
    align-items: center;
    @media only screen and (max-width: 480px) {
        flex-direction: column;
    }
`;

export default class CharDisplay extends React.Component {

    static propTypes = {
        qid: PropTypes.number
    }

    constructor(props) {
        super(props);
        this.state = {
            loading: true,
            character: null
        };
    }

    componentDidMount() {
        this.loadData();
    }

    async loadData() {
        const response = await fetch(`/content/character/${this.props.qid}`);
        if (!response.ok) {
            setTimeout(() => {
                this.loadData();
            }, 5);
            throw new Error(`An ${response.status} error has occured,
                retrying in 5 seconds.`);
        }

        // parse the response object into json
        const data = await response.json();
        // use the json object to update component states
        this.setState({ character: data, loading: false});
    }

    showLoadingView() {
        return <LoadingView />;
    }

    showContent() {
        const character = this.state.character;
        const definitions = character.definitions.map( v => 
            v.definition
        );
        return (
            <>
                <Row>
                    <CharItemPhonetic pinyin={[character.pinyin]}
                        audioURL=''
                        character={character.chinese}/>
                    <CharDefinition 
                        definitions={ definitions }
                    />
                </Row>
                <RelatedItems 
                    item={character.chinese}
                    itemType='word' />
                <BreakdownView type='radical'
                    componentURL={character.radicals}
                    memoryAid={character.memory_aid}/>
            </>
        );
    }


    render() {
        // Display a loading page while `this.state.loading == true`.
        return this.state.loading ? 
            this.showLoadingView() : this.showContent();
    }
}