import React from 'react';
import { render } from 'react-dom';

import App from './components/App.js';

const container = document.getElementById('learning-app');
const reactData = JSON.parse(document.getElementById('react-data').textContent);
render(
    <App {...reactData}/>, container
);