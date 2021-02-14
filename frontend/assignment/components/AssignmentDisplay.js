import React, {useState, useEffect} from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';

import HeaderView from "@assignment.components/HeaderView";
import ItemDisplayBody from "@assignment.components/ItemDisplayBody";
import useLoadAssignment from "@assignment.hooks/useLoadAssignment";
import ProgressBar from "@learning.components/CoreLearning/ProgressBar";

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
    display: flex;
    justify-content: space-around;
    height: 30px;
    width: 100%;
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

    const [specifiedObject, setSpecifiedObject] = useState(null);
    const [expanded, setExpanded] = useState(null);

    const onActionComplete = () => {
        window.location = `/learning/${props.qid}`;
    };

    const renderChinese = (obj) => {
        if (obj.type == 'radical')
            return <img src={obj.chinese}/>; // TODO make this smaller
        return obj.chinese;
    };

    const renderObjects = (objects) => {
        return objects.map((obj, index) => {
            // TODO make status that beautiful bar thing
            return (
                <RelatedContainer key={index}
                    onClick={()=>setSpecifiedObject(obj)}>
                    <RelatedContainerLeft className={'use-chinese'}>{renderChinese(obj)}</RelatedContainerLeft>
                    <RelatedContainerRight className={'use-chinese'}>/{obj.pinyin}/</RelatedContainerRight>
                </RelatedContainer>
            );
        });
    };

    const renderAssignment = () => {
        return (
            <ContentContainer>
                <HeaderView name={assignment.name} onActionComplete={onActionComplete}/>
                <ItemDisplayBody objectList={assignment.wordList}
                    specifiedObject={specifiedObject} />
                <Headings>Terms in this set</Headings>
                <ProgressBar {...assignment.progressBar}/>
                <div className={'collapsible use-chinese' + (expanded ? 'active': '')}>
                    {renderObjects(assignment.wordList)}
                    {renderObjects(assignment.characterList)}
                    {renderObjects(assignment.radicalList)}
                </div>    
                <div onClick={() => setExpanded(true)} className={'toggle'}>
                    <h4 style={{color: '#374C76'}}>expand</h4>
                    <i className={
                        'fas fa-chevron-down ' + 
                        (expanded ? 'inversed' : '')} style={{color: '#374C76'}} >
                    </i>
                </div>          
            </ContentContainer>
        );
    };

    if (assignment === null)
        return "loading assignment";
    else
        return renderAssignment();
}

AssignmentDisplay.propTypes = {
    qid: PropTypes.number,
}
