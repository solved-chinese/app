import React from 'react';
import 'core-js/stable';
import 'regenerator-runtime/runtime';
import PropTypes from 'prop-types';
import styled from 'styled-components';

import RelatedItems from './RelatedItems.js';
import { RadImage } from './RadicalDisplay/RadDisplay.js';

const Row = styled.div`
    display: inline-flex;
    min-width: 100%;
    justify-content: space-around;
    align-items: center;
    flex-wrap: wrap;
    margin-bottom: 20px;
`;

const MnemonicImageWrapper = styled.div`
    width: 35%;
    min-width: 60px;
    max-height: 150px;
    object-fit: contain;
    font-size: 2.25em;
    text-align: center;
`;

const RadDefinition = styled.h4`
    display: inline-block;
    width: 60%;
    font-size: 1.2em;
    text-align: center;
    min-width: 60px;
    margin-top: 15px;
`;

class BreakdownRad extends React.Component {

    static propTypes = {
        url: PropTypes.string
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
        const response = await fetch(this.props.url);
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
                    <MnemonicImageWrapper>
                        <RadImage url={imageUrl}
                            radical={chinese}/>
                    </MnemonicImageWrapper> 
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

const MemoryAidHeading = styled.h2`
    display: inline-block;
    width: 100%;
    color: var(--teritary-text);
    font-size: 0.9em;
    font-weight: 400;
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

function MemoryAidView(props) {
    return (
        <>
            <MemoryAidHeading>
                Memory Aid
            </MemoryAidHeading>
            <MemoryAidContent className='box-shadow'>
                {props.content}
            </MemoryAidContent>
        </>
    );
}

MemoryAidView.propTypes = {
    /** The associated memory aid sentence. */
    content: PropTypes.string.isRequired
};

export default class BreakdownView extends React.Component {

    static propTypes = {
        /** The type of breakdown components. */
        type: PropTypes.oneOf(['radical', 'word']),

        /** Urls of the breakdown components. */
        componentURL: PropTypes.arrayOf(PropTypes.string),

        /** The associated memory aid sentence. */
        memoryAid: PropTypes.string
    }

    constructor(props) {
        super(props);
        this.state = {
            show: false
        };
    }

    /**
     * Render radicals breakdown for each radical in the urls.
     * 
     * @param {[String]} urls 
     */
    renderBreakdownRad(urls) {
        return urls.map( url => 
            (
                <div key={url}
                    className='breakdown-card box-shadow'>
                    <BreakdownRad url={url} />
                </div>
            )
        );
    }

    // Since this function is used as event handler, use
    // arrow function to bind `this` to the class context.
    toggle = () => {
        this.setState( prev => ({show: !prev.show}));
    }

    render() {
        const toggleTitle = this.props.type + ' breakdown';

        return (
            <div className='breakdown-container'>
                <div 
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
                    )}>

                    {this.renderBreakdownRad(this.props.componentURL)}

                    <MemoryAidView
                        content={this.props.memoryAid}/>
                </div>
            </div>
        );
    }
}