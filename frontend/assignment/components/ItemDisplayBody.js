import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import ItemDisplay from '@learning.components/ItemDisplay/ItemDisplay';
import '@assignment.styles/ItemDisplayBody.css';


export default function ItemDisplayBody(props) {
    const [curObject, setCurObject] = useState(null);
    const [curPage, setCurPage] = useState(1);

    useEffect(() => {
        if (props.specifiedObject === null)
            return;
        const index = props.objectList.findIndex(obj =>
            obj === props.specifiedObject);
        if (index === -1)
            setCurPage(null);
        else
            setCurPage(index + 1);
        setCurObject(props.specifiedObject);
    }, [props.specifiedObject])

    useEffect(() => {
        if (curPage === null)
            return;
        setCurObject(props.objectList[curPage - 1]);
    }, [curPage])

    const displayItem = () => {
        if (curObject !== null)
            return <ItemDisplay qid={curObject.qid} type={curObject.type}
                                hasNext={false} onActionNext={null}/>;
    };

    return (
        <>
            {displayItem()}
            <PageControl maxPage={props.objectList.length}
                         isTransitioning={false}
                         curPage={curPage} setCurPage={setCurPage}
            />
        </>
    );
}

ItemDisplayBody.propTypes = {
    objectList: PropTypes.arrayOf(PropTypes.object),
    specifiedObject: PropTypes.object,
};

ItemDisplayBody.defaultProps = {
    specifiedObject: null,
}

const PageControlContainer = styled.div`
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    justify-content: space-between;
    align-items: center;
    margin: 10px auto;
    width: 100px;
`;

function PageControl(props) {
    const pageControlLabelString = `${props.curPage}/${props.maxPage}`;

    const handleClick = (dir) => {
        return () => {
            const newPage = props.curPage + dir;
            if (1 <= newPage && newPage <= props.maxPage)
                props.setCurPage(newPage);
        }
    };

    if (props.curPage !== null)
        return (
            <PageControlContainer>
                <i className='fas fa-chevron-left page-control' onClick={handleClick(-1)}/>
                <p className='page-control label'>{pageControlLabelString}</p>
                <i className='fas fa-chevron-right page-control' onClick={handleClick(1)}/>
            </PageControlContainer>
        );
    return null;
}

PageControl.propTypes = {
    curPage: PropTypes.number,
    setCurPage: PropTypes.func.isRequired,
    maxPage: PropTypes.number.isRequired,
    isTransitioning: PropTypes.bool.isRequired
};