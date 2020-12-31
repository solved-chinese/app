import React from 'react';
import CharItemPhonetic from './CharItemPhonetic.js';
import CharDefinition from './CharDefinition.js';
import styled from 'styled-components';
import RelatedItems from './RelatedItems.js';
import BreakdownView from './BreakdownView';
import PropTypes from 'prop-types';
import LoadingView from './LoadingView.js';
import 'core-js/stable';
import 'regenerator-runtime/runtime';

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
        return (
            <>
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
                <RelatedItems 
                    item='someword'
                    itemType='word' />
                <BreakdownView type='radical' />
            </>
        );
    }


    render() {
        // Display a loading page while `this.state.loading == true`.
        return this.state.loading ? 
            this.showLoadingView() : this.showContent();
    }
}