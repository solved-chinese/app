import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import ItemDisplay from '@learning.components/ItemDisplay/ItemDisplay';
import '@assignment.styles/ItemDisplayBody.css';


export default function ItemDisplayBody(props) {
    const [curPage, setCurPage] = useState(1);

    useEffect(() => {
        const index = props.objectList.findIndex(obj =>
            obj === props.curObject);
        if (index === -1)
            setCurPage(null);
        else if (index !== curPage)
            setCurPage(index + 1);
    }, [props.curObject])

    useEffect(() => {
        if (curPage === null)
            return;
        if (props.objectList[curPage -1] !== props.curObject)
            props.setCurObject(props.objectList[curPage - 1]);
    }, [curPage])

    const displayItem = () => {
        if (props.curObject)
            return <ItemDisplay qid={props.curObject.qid}
                                type={props.curObject.type}
                                displayRef={props.displayRef}
                                hasNext={false} onActionNext={null}/>;
    };

    return (
        <>
            <PageControl maxPage={props.objectList.length}
                         isTransitioning={false}
                         curPage={curPage} setCurPage={setCurPage}
            />
            {displayItem()}
        </>
    );
}

ItemDisplayBody.propTypes = {
    objectList: PropTypes.arrayOf(PropTypes.object),
    curObject: PropTypes.object,
    setCurObject: PropTypes.func,
};

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
                <i className='fas fa-chevron-left page-control'
                   onClick={handleClick(-1)}
                   style={{cursor: 'pointer'}}
                />
                <p className='page-control label'>{pageControlLabelString}</p>
                <i className='fas fa-chevron-right page-control'
                   onClick={handleClick(1)}
                   style={{cursor: 'pointer'}}
                />
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