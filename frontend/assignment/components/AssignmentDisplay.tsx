import React, {useState, useRef} from 'react';
import styled from 'styled-components';

import HeaderView from '@assignment.components/HeaderView';
import ItemDisplayBody from '@assignment.components/ItemDisplayBody';
import useLoadAssignment from '@assignment.hooks/useLoadAssignment';
import ProgressBar from '@learning.components/CoreLearning/ProgressBar';

import '@assignment.styles/AssignmentDisplay.css';
import {Assignment, SimpleContentObject} from '@interfaces/Assignment';

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

const Headings = styled.h1`
    font-size: 1.5em;
    font-weight: 600;
`;

type Props = {
    qid: number
}

const AssignmentDisplay = (props: Props): JSX.Element => {
    const [curObject, setCurObject] = useState<SimpleContentObject | null>(null);
    const assignment = useLoadAssignment(`/learning/api/assignment/${props.qid}`, (assignment => {
        setCurObject(assignment.wordList[0]);
    }));
    const displayRef = useRef<HTMLDivElement>(null);

    const onActionComplete = () => {
        window.location.href = `/learning/${props.qid}`;
    };

    const renderChinese = (obj: SimpleContentObject) => {
        if (obj.type === 'radical')
            return <img src={obj.chinese} alt={obj.chinese}/>; // TODO make this smaller
        return obj.chinese;
    };

    const renderObjects = (objects: SimpleContentObject[]) => {
        return objects.map((obj, index) => {
            // TODO make status that beautiful bar thing
            return (
                <RelatedContainer key={index}
                    onClick={()=>{
                        setCurObject(obj);
                        displayRef?.current?.focus();
                    }}
                    className={'use-chinese'}
                    style={obj === curObject? {backgroundColor: '#EBEBEB'} : {}}
                >
                    &nbsp;&nbsp;&nbsp;&nbsp;
                    {renderChinese(obj)} &nbsp;&nbsp;
                    {obj.pinyin? '/' + obj.pinyin + '/' : null}&nbsp;&nbsp;
                    {obj.definition}
                </RelatedContainer>
            );
        });
    };

    const renderAssignment = (assignment: Assignment) => {
        return (
            <ContentContainer>
                <HeaderView
                    name={assignment.name}
                    onActionComplete={onActionComplete}
                />
                <ProgressBar {...assignment.progressBar}/>
                <ItemDisplayBody
                    objectList={assignment.wordList}
                    displayRef={displayRef}
                    curObject={curObject!}
                    setCurObject={object => setCurObject(object)}
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
            </ContentContainer>
        );
    };

    if (assignment === null)
        return (<>loading assignment</>);
    else
        return renderAssignment(assignment);
};

export default AssignmentDisplay;
