
import React, { useState } from 'react';
import Modal from 'react-modal';
import styled from 'styled-components';
import PropTypes from 'prop-types';
import CharDisplay from
    '@learning.components/ItemDisplay/CharacterDisplay/CharDisplay';

import '@learning.styles/ItemDisplay.css';
import Constant from '@utils/constant';

//Styles for Popup
const ModalStyle = {
    overlay: {
        backgroundColor: 'rgba(116, 116, 116, 0.3)'
    },
    content: {
        position: 'absolute',
        top: '100px',
        left: '0px',
        right: '0px',
        height: 'auto',
        maxHeight: '70vh',
        bottom: 'auto',

        display: 'inline-block',
        maxWidth: '700px',
        widths: '100%',
        margin: '0 auto',

        backgroundColor: 'white',
        width: '90%',
        padding: '25px 50px',

        boxShadow: '2px 2px 6px 2px #30354514',
        borderRadius: '5px',
    }
};

//New 'plus' button
const PlusButton = styled.img`
    position: relative;
    bottom: 100%;
    left: 90%;
    cursor: pointer;
    transform: scale(0.6);
    &:hover{
        transform: scale(0.7);
        transition: 200ms ease-in-out;
    }
`;
//New 'close' button
const CloseButton = styled.i`
    position: relative;
    top: 0;
    left: 100%;
    cursor: grab;
    &:hover{
        transform: scale(1.2);
        transition: 200ms ease-in-out;
    }
`;

/**
 * Renders a component that will bring up a popup modal
 * that displays an item.
 * a word breakdown.
 * @param {String} props.contentURL URL of the item to be presented in the popup modal.
 * @param {String} props.type The kind of item in contentURL.
 * @return {JSX.Element}
 */
export default function ItemDisplayPopup(props) {

    const [ModalState, setModalState] = useState(false);

    Modal.setAppElement(`#${Constant.ROOT_ELEMENT_ID}`);

    const renderItem = () => {

    };

    return (
        <>
            <PlusButton
                src="/static/images/small-icons/read-more-red.svg"
                alt="read more"
                onClick={() => setModalState(true)}
            />

            <div>
                <Modal
                    closeTimeoutMS={500} 
                    style={ModalStyle} 
                    isOpen={ModalState} 
                    onRequestClose={() => setModalState(false)}
                >
                    <CloseButton 
                        className='fas fa-times' 
                        onClick={() => setModalState(false)} 
                    />
                    <CharDisplay
                        url={props.contentURL}
                        autoExpandBreakdown={true}
                    />
                </Modal>
            </div>
        </>
    );
}

ItemDisplayPopup.propTypes = {
    /** URL of the item presented in the popup modal. */
    contentURL: PropTypes.string.isRequired,

    /** The kind of item in contentURL. */
    type: PropTypes.oneOf(['word', 'character', 'radical'])
};