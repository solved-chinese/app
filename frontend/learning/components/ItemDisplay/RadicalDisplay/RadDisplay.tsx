import React from 'react';
import styled from 'styled-components';

import RelatedItems from '@learning.components/ItemDisplay/RelatedItems';
import LoadingView from '@learning.components/ItemDisplay/LoadingView';
import useLoadRad from '@learning.hooks/useLoadRad';

import { Radical } from '@interfaces/CoreItem';

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
    flex-grow: 2;
    font-size: 1.75em;
    text-align: center;
    min-width: 200px;
    margin-top: 20px;
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

type Props = {
    /**
     * The radical object to be rendered, if not provided,
     * the url param will be used to fetch the object.
     */
    radical?: Radical,

    /**
     * URL of the radical to be rendered, if it
     * is not provided, then the qid is used to construct
     * the url.
     */
    url?: string,

    /**
     * The query id of the radical to be rendered, will
     * be omitted if url is present and not null.
     */
    qid?: number,
}

/**
 * The main function that renders a radical view.
 */
const RadDisplay = (props: Props): JSX.Element => {

    const radical = props.radical == null?
        useLoadRad(props.url == null ?
            `/content/radical/${props.qid}` : props.url
        ) : props.radical;

    const audio = radical != null ? 
        new Audio(radical.audioUrl) :
        null;

    const renderRadical = (radical: Radical) => {
        const chinese = radical.chinese;
        const def = radical.definition;
        const explanation = radical.explanation;
        const imageUrl = radical.image;

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
                                    onClick={() => audio?.play()}
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
        return <LoadingView />;
    } else {
        return renderRadical(radical);
    }
};

export default RadDisplay;

type RadImageProps = {
    /** Url of the radical image */
    url: string,

    /**
     * The text radical to be displayed, in case
     * of an error.
     */
    radical: string
}

type RadImageState = {
    errored: boolean
}

export class RadImage extends React.Component<RadImageProps, RadImageState> {

    constructor(props: RadImageProps) {
        super(props);
        this.state = {
            errored: false
        };
    }

    /**
     * Callback function when there's an error loading
     * the img tag.
     */
    onError = (): void => {
        this.setState({ errored: true });
    }

    render(): JSX.Element {
        const {radical, url} = this.props;
        return this.state.errored ? <>radical</> : (
            <img src={url} alt={radical} onError={this.onError} />
        );
    }
}
