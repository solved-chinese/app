import React from 'react';
import styled from 'styled-components';
import PropTypes from 'prop-types';

import RelatedItems from '@ItemDisplay/RelatedItems.js';

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

    static propTypes = {
        qid: PropTypes.number
    }

    constructor(props) {
        super(props);
        this.state = {
            loading: true,
            radical: null
        };
    }

    componentDidMount() {
        this.loadData();
    }

    async loadData() {
        const response = await fetch(`/content/radical/${this.props.qid}`);
        if (!response.ok) {
            setTimeout(() => {
                this.loadData();
            }, 5);
        }

        const data = await response.json();
        this.setState({ loading: false, radical: data});
    }

    renderRadical = (radical) => {
        const chinese = radical.chinese;
        const def = radical.explanation;
        const imageUrl = radical.image;

        return (
            <>
                <Row>
                    <MnemonicImage src={imageUrl}/>
                    <RadDefinition className='use-serifs'>
                        {def}
                    </RadDefinition>
                </Row>
                <RelatedItems
                    item={chinese}
                    itemType='character' />
            </>
        );
    }

    render() {
        const loading = this.state.loading;
        return loading ?
            'Error fetching character data, retrying' :
            this.renderRadical(this.state.radical);
    }
}

export class RadImage extends React.Component {

    static propTypes = {
        /** Url of the radical image */
        url: PropTypes.string,

        /** The text radical to be displayed, in case
         * of an error.
         */
        radical: PropTypes.string
    }

    constructor(props) {
        super(props);
        this.state = {
            errored: false
        };
    }

    /** Callback function when there's an error loading
     * the img tag.
     */
    onError = () => {
        this.setState({ errored: true });
    }

    render() {
        const {radical, url} = this.props;
        return this.state.errored ? radical : (
            <img src={url} onError={this.onError} />
        );
    }
}