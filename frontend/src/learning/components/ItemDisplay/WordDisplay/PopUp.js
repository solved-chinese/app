
import React, { useState } from 'react';
import Modal from 'react-modal';
import styled from 'styled-components';
import PropTypes from 'prop-types';
import CharDisplay from '../CharacterDisplay/CharDisplay';

//Changed root-element-id.
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

        boxShadow: '2px 2px 6px 2px #30354514',
        borderRadius: '5px',
    }
};

//New 'plus' button
const PlusButton = styled.i`
    position: relative;
    top: auto;
    bottom: 200%;
    left: 93%;
    margin: 0 10px;
    cursor: grab;
    &:hover{
        transform: scale(1.4);
        transition: 400ms ease;
    }
`;
//New 'close' button
const CloseButton1 = styled.i`
    width: 100%;
    text-align: right;
    cursor: grab;
    margin: 10px 0;
    &:hover{
        transform: scale(1.4);
        transition: 400ms ease;
    }
    
`;


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
                    <CloseButton1 
                        className='fas fa-times' 
                        onClick={() => setModalState(false)} 
                    />
                    <CharDisplay
                        qid={props.qid}
                    />
                </Modal>
            </div>
        </>
    );
}

PopUp.propTypes = {
    qid: PropTypes.number
};