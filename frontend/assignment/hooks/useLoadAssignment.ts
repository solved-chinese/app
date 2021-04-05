import { useState, useEffect } from 'react';
import 'core-js/stable';
import 'regenerator-runtime/runtime';
import camelcaseKeys from 'camelcase-keys';

import { Assignment } from '@interfaces/Assignment';

/**
 * Load a Assignment from URL, returns null when it is still
 * loading. The function will automatically reload the
 * returned assignment if the URL that's passed in changes.
 */
export default function useLoadAssignment(url: string): Assignment {

    const [assignment, setAssignment] = useState(null);

    const loadData = async () => {
        const response = await fetch(url);
        if (!response.ok) {
            if (response.status === 404) { return; }
        } else {
            // parse the response object into json
            const data = await response.json();
            // use the json object to update component states
            setAssignment(camelcaseKeys(data, {deep: true}));
        }
    };

    // If the url changes, reload data
    useEffect(loadData, [url]);
    return assignment;
}