import React from 'react';
import styled from 'styled-components';
import PropTypes from 'prop-types';

import RelatedItems from '@learning.components/ItemDisplay/RelatedItems';
import LoadingView from '@learning.components/ItemDisplay/LoadingView';

import useLoadRad from '@learning.hooks/useLoadRad';

import '@learning.styles/ItemDisplay.css';

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

/** The main function that renders a radical view. */
export default function RadDisplay(props) {

    const radical = useLoadRad(
        props.url == null ?
            `/content/radical/${props.qid}` :
            props.url
    );

    const renderRadical = (radical) => {
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
                    items={radical.related_characters}
                    itemType='character' />
            </>
        );
    };

    if (radical === null) {
        return <LoadingView />;
    } else {
        return renderRadical(radical);
    }
}

RadDisplay.propTypes = {
    /** URL of the radical to be rendered, if it 
     * is not provided, then the qid is used to construct
     * the url. */
    url: PropTypes.string,

    /** The query id of the radical to be rendered, will
     * be omitted if url is present and not null. */
    qid: PropTypes.number,
};

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