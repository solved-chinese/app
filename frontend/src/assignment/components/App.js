import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import HeaderView from './HeaderView';
import ItemDisplayBody from './ItemDisplayBody';

const ContentContainer = styled.div`
    max-width: 900px;
    margin: 20px auto;
    
    @media only screen and (max-width: 480px) {
      margin: 20px 0;
    }
`;

export default class App extends React.Component {
    render() {
        return (
            <ContentContainer>
                <HeaderView/>
                <ItemDisplayBody/>
            </ContentContainer>
        );
    }
}