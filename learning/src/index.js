import App from './components/App';
import React from 'react';
import { render } from 'react-dom';
import {
    BrowserRouter as Router,
    Route
} from 'react-router-dom';

const container = document.getElementById('learning-app');
render(
    <Router>
        <Route path='/learning' component={App} />
    </Router>, 
    container);