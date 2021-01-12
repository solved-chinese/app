
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
        position: 'absolute',
        maxWidth: '705px',
        margin: '0 auto',
        padding: '0',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        // Make not cover full screen
        top: '15%',
        bottom: 'auto',
        height: 'auto',
        // Try to add box-shadow    
        border: '1px solid white',
        borderRadius: '10px',
        boxShadow: '30px 30px 30px 30px #30354512',
        // Disables overflow 
        overflow: 'hidden',
    }
};

// //Old '+' bottom
// const PopButton = styled.button`
//   background: none;
//   position: relative;
//   top: auto;
//   bottom: 200%;
//   left: 94%;
//   border: 1px solid white;
//   border-radius: 3px;
//   cursor: grab;
// `;
// //Old 'x' bottom
// const CloseButton = styled.button`
//   background: white;
//   position: relative;
//   border: 1px solid white;
//   border-radius: 3px;
//   cursor: grab;
// `;

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
    border: 1px solid white;
    border-radius: 3px;
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
                <Modal closeTimeoutMS={500} style={ModalStyle} isOpen={ModalState} onRequestClose={() => setModalState(false)}>
                    <CloseButton1 className='fas fa-times' onClick={() => setModalState(false)}/>
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