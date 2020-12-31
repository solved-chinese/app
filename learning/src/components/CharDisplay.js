import React from 'react';
import CharItemPhonetic from './CharItemPhonetic.js';
import CharDefinition from './CharDefinition.js';
import styled from 'styled-components';
import RelatedItems from './RelatedItems.js';
import BreakdownView from './BreakdownView';
import PropTypes from 'prop-types';
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
            loading: true
        };
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
        return this.state.loading ? 
            this.showLoadingView() : this.showContent();
    }
}