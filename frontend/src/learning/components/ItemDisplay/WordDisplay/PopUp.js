
import React, { useState } from 'react';
import Modal from 'react-modal';
import styled from 'styled-components';
import PropTypes from 'prop-types';
import CharDisplay from '../CharacterDisplay/CharDisplay';

Modal.setAppElement('#learning-app');

//Styles for Popup
const ModalStyle = {
    overlay:{
        backgroundColor: 'rgba(116, 116, 116, 0.3)'
    },
    content:{
        maxWidth: '800px',
        marginTop: '60px',
        marginBottom: '60px',
        margin: 'auto',
        backgroundColor: 'white',
        width: '100%',
        padding: '25px 50px',

        // Make not cover full screen
        top: '15%',
        bottom: 'auto',
        height: 'auto',
        maxHeight: '70vh',

        boxShadow: '2px 2px 6px 2px #30354514',
        borderRadius: '5px',
    }
};

//New 'plus' button
const PlusButton = styled.i`
    position: relative;
    top: 0;
    left: 95%;
    margin: 5px;
    cursor: pointer;
    &:hover{
        transform: scale(1.2);
        transition: 400ms ease-in-out;
    }
`;
//New 'close' button
const CloseButton = styled.i`
    position: relative;
    top: 0;
    left: 95%;
    margin: 5px;
    cursor: pointer;
    &:hover{
        transform: scale(1.2);
        transition: 400ms ease-in-out;
    }
`;

/**
 * Renders a popup modal that displays a character in
 * a word breakdown.
 * @param {{contentURL: String}} props 
 */
export default function PopUp(props) {

    const [ModalState, setModalState] = useState(false);

    return (
        <>
            <PlusButton className = 'fas fa-plus' onClick={() => setModalState(true)}/>
            
            <div>
                {/* Modal now displays CharDisplay */}
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
                    />
                </Modal>
            </div>
        </>
    );
}

PopUp.propTypes = {
    /** URL of the character presented in the popup modal. */
    contentURL: PropTypes.string.isRequired
};