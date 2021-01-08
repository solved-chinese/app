
import React, { useState } from 'react';
import Modal from 'react-modal';
import styled from 'styled-components';
import RadicalDisplay from '../RadicalDisplay/RadDisplay';
import WordDisplay from './WordDisplay';
import PropTypes from 'prop-types';

//Can't render if uncomment the following line. Why?
//Modal.setAppElement('#root');

//Styles for Popup
const DivStyle = {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'grey',
};
const ModalStyle = {
    overlay:{
        backgroundColor: 'rgba(255, 255, 255, 0.4)'
    },
    content:{
        position: 'absolute',
        maxWidth: '705px',
        margin: '0 auto',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        border: '1px solid white',
        borderRadius: '10px',
        padding: '0',
        
    }
};

//Style for '+' bottom
const PopButton = styled.button`
  background: none;
  position: relative;
  top: auto;
  bottom: 200%;
  left: 94%;
  border: 1px solid white;
  border-radius: 3px;
  cursor: grab;
`;
//Style for 'x' bottom
const CloseButton = styled.button`
  background: white;
  position: relative;
  border: 1px solid white;
  border-radius: 3px;
  cursor: grab;
`;


export default function PopUp(props) {

  
    const [ModalState, setModalState] = useState(false);
    return (
        <>
            <PopButton onClick={() => setModalState(true)}>
              +
            </PopButton>
            <div style={DivStyle}>
                <Modal closeTimeoutMS={500} style={ModalStyle} isOpen={ModalState} onRequestClose={() => setModalState(false)}>
                    <CloseButton onClick={() => setModalState(false)}>
                x
                    </CloseButton>
                    <RadicalDisplay
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