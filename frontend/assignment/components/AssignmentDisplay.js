import React, {useState, useEffect, useRef} from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';

import HeaderView from '@assignment.components/HeaderView';
import ItemDisplayBody from '@assignment.components/ItemDisplayBody';
import useLoadAssignment from '@assignment.hooks/useLoadAssignment';
import ProgressBar from '@learning.components/CoreLearning/ProgressBar';

import '@assignment.styles/AssignmentDisplay.css';

// Containers
const ContentContainer = styled.div`
    max-width: 900px;
    margin: 20px auto;
    
    @media only screen and (max-width: 480px) {
    margin: 20px 0;
    }
`;

const RelatedContainer = styled.div`
    max-width: 900px;
    height: 40px;
    width: 100%;
    overflow: hidden;
    font-weight: 600;
    font-size: 1.2em;
`;

const RelatedContainerLeft = styled.div`
    column-width: 20%;
    margin-right: 10px;
    font-weight: 600;
    font-size: 1em;
`;

const RelatedContainerRight = styled.div`
    column-width: auto;
    overflow: hidden;
    font-weight: 600;
    font-size: 1em;
`;

const Headings = styled.h1`
    font-size: 1.5em;
    font-weight: 600;
`;

export default function AssignmentDisplay(props) {
    const assignment = useLoadAssignment(`/learning/api/assignment/${props.qid}`);
    const displayRef = useRef(null);

    const [curObject, setCurObject] = useState(null);
    // const [expanded, setExpanded] = useState(false);

    const onActionComplete = () => {
        window.location = `/learning/${props.qid}`;
    };

    const renderChinese = (obj) => {
        if (obj.type === 'radical')
            return <img src={obj.chinese}/>; // TODO make this smaller
        return obj.chinese;
    };

    const renderObjects = (objects) => {
        return objects.map((obj, index) => {
            // TODO make status that beautiful bar thing
            return (
                <RelatedContainer key={index} align='left'
                    onClick={()=>{
                        setCurObject(obj);
                        displayRef.current.focus();
                    }}
                    className={'use-chinese'}
                    style={obj === curObject? {backgroundColor: '#EBEBEB'} : null}
                >
                    &nbsp;&nbsp;&nbsp;&nbsp;
                    {renderChinese(obj)} &nbsp;&nbsp;
                    {obj.pinyin? '/' + obj.pinyin + '/' : null}&nbsp;&nbsp;
                    {obj.definition}
                </RelatedContainer>
            );
        });
    };

    const renderAssignment = () => {
        return (
            <ContentContainer>
                <HeaderView name={assignment.name} onActionComplete={onActionComplete}/>
                <ProgressBar {...assignment.progressBar}/>
                <ItemDisplayBody objectList={assignment.wordList}
                    displayRef={displayRef}
                    curObject={curObject}
                    setCurObject={setCurObject}
                />
                <br/><br/>
                <Headings>Terms in this set ({assignment.wordList.length})</Headings>
                <div className={'use-chinese'}>
                    {renderObjects(assignment.wordList)}
                    {assignment.characterList.length? <h4>Bonus characters</h4>:null}
                    {renderObjects(assignment.characterList)}
                    {assignment.radicalList.length? <h4>Bonus radicals</h4>:null}
                    {renderObjects(assignment.radicalList)}
                </div>    
                {/*<div onClick={() => setExpanded(true)} className={'toggle'}>*/}
                {/*    <h4 style={{color: '#374C76'}}>expand</h4>*/}
                {/*    <i className={*/}
                {/*        'fas fa-chevron-down ' + */}
                {/*        (expanded ? 'inversed' : '')} style={{color: '#374C76'}} >*/}
                {/*    </i>*/}
                {/*</div>          */}
            </ContentContainer>
        );
    };

    if (assignment === null)
        return 'loading assignment';
    else
        return renderAssignment();
}

AssignmentDisplay.propTypes = {
    qid: PropTypes.number,
};
