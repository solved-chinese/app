import { useState, useEffect } from 'react';
import camelcaseKeys from 'camelcase-keys';

import { Assignment } from '@interfaces/Assignment';

/**
 * Load a Assignment from URL, returns null when it is still
 * loading. The function will automatically reload the
 * returned assignment if the URL that's passed in changes.
 * Optionally, a callback function can be passed in, which will be executed
 * before the state update happens.
 */
const useLoadAssignment = (url: string, completion?: (assignment: Assignment)=>void): Assignment | null => {

    const [assignment, setAssignment] = useState<Assignment | null>(null);

    const loadData = async (): Promise<Assignment | null> => {
        const response = await fetch(url);
        if (!response.ok) {
            return null;
        } else {
            // parse the response object into json
            const data = await response.json();
            // use the json object to update component states
            return camelcaseKeys(data, {deep: true});
        }
    };

    // If the url changes, reload data
    useEffect(() => {
        loadData().then(assignment => {
            if (assignment) {
                completion && completion(assignment);
                setAssignment(assignment);
            }
        });
    }, [url]);
    return assignment;
};

export default useLoadAssignment;
