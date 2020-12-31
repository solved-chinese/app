import App from './components/App';
import React from 'react';
import { render } from 'react-dom';
import {
    BrowserRouter as Router,
} from 'react-router-dom';

const container = document.getElementById('learning-app');
render(
    <Router>
        <App />
    </Router>, container);