import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import ItemDisplay from '@learning.components/ItemDisplay/ItemDisplay';
import '@assignment.styles/ItemDisplayBody.css';

export default function ItemDisplayBody(props) {
    return (
        <>
            <ItemDisplay qid={1} type={'word'}  hasNext={false} onActionNext={null}/>
            <PageControl currPage={1} maxPage={20} isTransitioning={false}/>
        </>
    );
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
    const pageControlLabelString = `${props.currPage}/${props.maxPage}`;

    return (
        <PageControlContainer>
            <i className='fas fa-chevron-left page-control'/>
            <p className='page-control label'>{pageControlLabelString}</p>
            <i className='fas fa-chevron-right page-control'/>
        </PageControlContainer>
    );
}

PageControl.propTypes = {
    currPage: PropTypes.number.isRequired,
    maxPage: PropTypes.number.isRequired,
    isTransitioning: PropTypes.bool.isRequired
};