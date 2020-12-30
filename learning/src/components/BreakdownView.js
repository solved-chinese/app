import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import RelatedItems from './RelatedItems.js';

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
    min-width: 60px;
    max-height: 150px;
    object-fit: contain;
`;

const RadDefinition = styled.h4`
    display: inline-block;
    width: 60%;
    font-size: 1.2em;
    text-align: center;
    min-width: 60px;
    margin-top: 20px;
`;

class BreakdownRad extends React.Component {
    render() {
        return (
            <>
                <Row>
                    <MnemonicImage 
                        src='/media/mnemonic_image/R0004.png' />
                    <RadDefinition className='use-serifs'>
                        perhaps a longer definition
                    </RadDefinition>
                </Row>
                <RelatedItems 
                    item='somechar'
                    itemType='character' />
            </>
        );
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
        type: PropTypes.oneOf(['radical', 'word'])
    }

    constructor(props) {
        super(props);
        this.state = {
            show: false
        };
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
                    <div className='breakdown-card 
                        box-shadow'>
                        <BreakdownRad />
                    </div>
                    <div className='breakdown-card 
                        box-shadow'>
                        <BreakdownRad />
                    </div>
                    <MemoryAidView
                        content='A child(子) sits under the roof of
                        a school building to learn(学).' />
                </div>
            </div>
        );
    }
}