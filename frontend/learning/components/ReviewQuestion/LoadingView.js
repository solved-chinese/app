import React from 'react';
import ContentLoader from 'react-content-loader';
import styled from 'styled-components';


const LoadingViewContainer = styled.div`
    padding-top: 25vh;

    width: 350px;
    margin: auto;
`;

/**
 * Returns an animated loading screen.
 * @param {Object} props 
 * @returns {React.Component} an animated loading screen
 */
const LoadingView = (props) => (
    <LoadingViewContainer>
        <ContentLoader 
            speed={2}
            width={350}
            height={84}
            viewBox="0 0 350 84"
            backgroundColor="#f3f3f3"
            foregroundColor="#ecebeb"
            {...props}
        >
            <rect x="0" y="0" rx="3" ry="3" width="67" height="11" /> 
            <rect x="76" y="0" rx="3" ry="3" width="140" height="11" /> 
            <rect x="127" y="48" rx="3" ry="3" width="53" height="11" /> 
            <rect x="187" y="48" rx="3" ry="3" width="72" height="11" /> 
            <rect x="18" y="48" rx="3" ry="3" width="100" height="11" /> 
            <rect x="0" y="71" rx="3" ry="3" width="37" height="11" /> 
            <rect x="18" y="23" rx="3" ry="3" width="140" height="11" /> 
            <rect x="166" y="23" rx="3" ry="3" width="173" height="11" />
        </ContentLoader>
    </LoadingViewContainer>

);

export default LoadingView;

