import React from 'react';
import { render } from 'react-dom';
import App from '@learning.components/App';
import Constant from '@utils/constant';
import * as Sentry from '@sentry/react';
import { Integrations } from '@sentry/tracing';

Sentry.init({
    dsn: 'https://ec26038446614e378a2a2a990bf4c501@o479182.ingest.sentry.io/5712116',
    integrations: [new Integrations.BrowserTracing()],

    // Set tracesSampleRate to 1.0 to capture 100%
    // of transactions for performance monitoring.
    // We recommend adjusting this value in production
    tracesSampleRate: 1.0,
});

const container = document.getElementById(Constant.ROOT_ELEMENT_ID);
const reactData = JSON.parse(document.getElementById('react-data')?.textContent as string);
render(
    <App {...reactData}/>, container
);