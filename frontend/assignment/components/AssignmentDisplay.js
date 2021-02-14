import React, {useState, useEffect} from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';

import HeaderView from "@assignment.components/HeaderView";
import ItemDisplayBody from "@assignment.components/ItemDisplayBody";
import useLoadAssignment from "@assignment.hooks/useLoadAssignment";
import ProgressBar from "@learning.components/CoreLearning/ProgressBar";


const ContentContainer = styled.div`
    max-width: 900px;
    margin: 20px auto;
    
    @media only screen and (max-width: 480px) {
      margin: 20px 0;
    }
`;


export default function AssignmentDisplay(props) {
    const assignment = useLoadAssignment(`/learning/api/assignment/${props.qid}`);

    const [specifiedObject, setSpecifiedObject] = useState(null);

    const onActionComplete = () => {
        window.location = `/learning/${props.qid}`;
    };

    const renderChinese = (obj) => {
        if (obj.type == 'radical')
            return <img src={obj.chinese} />; // TODO make this smaller
        return obj.chinese;
    };

    const renderObjects = (objects) => {
        return objects.map((obj, index) => {
            // TODO make status that beautiful bar thing
            return (
                <div key={index}
                        onClick={()=>setSpecifiedObject(obj)}>
                    {obj.status} {renderChinese(obj)} {obj.pinyin}
                </div>
            );
        });
    };

    const renderAssignment = () => {
        return (
            <ContentContainer>
                <HeaderView name={assignment.name} onActionComplete={onActionComplete}/>
                <ItemDisplayBody objectList={assignment.wordList}
                                 specifiedObject={specifiedObject} />
                <ProgressBar {...assignment.progressBar}/>
                words:
                {renderObjects(assignment.wordList)}
                characters:
                {renderObjects(assignment.characterList)}
                radicals:
                {renderObjects(assignment.radicalList)}
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
