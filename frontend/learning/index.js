import React from 'react';
import { render } from 'react-dom';

import App from './components/App.js';
import Constant from '@utils/constant';

const container = document.getElementById(Constant.ROOT_ELEMENT_ID);
const reactData = JSON.parse(document.getElementById('react-data').textContent);
render(
    <App {...reactData}/>, container
);