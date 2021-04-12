import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import ItemDisplay from '@learning.components/ItemDisplay/ItemDisplay';
import '@assignment.styles/ItemDisplayBody.css';
import {SimpleContentObject} from '@interfaces/Assignment';

type ItemDisplayBodyProps = {
    objectList: SimpleContentObject[],
    curObject: SimpleContentObject,
    setCurObject: (object: SimpleContentObject)=>void,
    displayRef: React.RefObject<HTMLDivElement>
}

const ItemDisplayBody = (props: ItemDisplayBodyProps): JSX.Element => {
    const [curPage, setCurPage] = useState<number>(1);
    useEffect(() => {
        const index = props.objectList.findIndex(obj =>
            obj === props.curObject);
        if (index === -1)
            console.error('Unable to find index for the current object');
            // TODO: Error Handling
        else if (index !== curPage)
            setCurPage(index + 1);
    }, [props.curObject]);

    useEffect(() => {
        if (curPage == null)
            return;
        if (props.objectList[curPage -1] !== props.curObject)
            props.setCurObject(props.objectList[curPage - 1]);
    }, [curPage]);

    const displayItem = () => {
        if (props.curObject)
            return <ItemDisplay
                qid={props.curObject.qid}
                type={props.curObject.type}
                displayRef={props.displayRef}
                hasNext={false}
            />;
    };

    return (
        <>
            <PageControl
                maxPage={props.objectList.length}
                isTransitioning={false}
                curPage={curPage}
                setCurPage={setCurPage}
            />
            {displayItem()}
        </>
    );
};

export default ItemDisplayBody;


const PageControlContainer = styled.div`
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    justify-content: space-between;
    align-items: center;
    margin: 10px auto;
    width: 100px;
`;

type PageControlProps = {
    curPage: number,
    setCurPage: (arg0: number)=>void,
    maxPage: number,
    isTransitioning: boolean
}

export const PageControl = (props: PageControlProps): JSX.Element | null => {
    const pageControlLabelString = `${props.curPage}/${props.maxPage}`;

    const handleClick = (dir: number) => {
        return () => {
            const newPage = props.curPage + dir;
            if (1 <= newPage && newPage <= props.maxPage)
                props.setCurPage(newPage);
        };
    };

    if (props.curPage !== null)
        return (
            <PageControlContainer>
                <i
                    className='fas fa-chevron-left page-control'
                    onClick={handleClick(-1)}
                    style={{cursor: 'pointer'}}
                />
                <p className='page-control label'>{pageControlLabelString}</p>
                <i
                    className='fas fa-chevron-right page-control'
                    onClick={handleClick(1)}
                    style={{cursor: 'pointer'}}
                />
            </PageControlContainer>
        );
    return null;
};
