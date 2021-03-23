import { useState, useEffect } from 'react';
import 'core-js/stable';
import 'regenerator-runtime/runtime';
import camelcaseKeys from 'camelcase-keys';

import { Character } from '@interfaces/CoreItem';
import Constant from '@utils/constant';

/**
 * Load a character from URL, returns null when it is still
 * loading. The function will automatically reload the
 * returned character if the URL that's passed in changes. 
 * Reattempt in 5 seconds if loading fails.
 * @param {String} url 
 * 
 * @return {Character | null}
 */
export default function useLoadChar(url) {

    const [character, setCharacter] = useState(null);

    const loadData = async () => {
        const response = await fetch(url);
        if (!response.ok) {
            if (response.status === 404) { return; }
            setTimeout(loadData, Constant.REQUEST_TIMEOUT);
        } else {
            // parse the response object into json
            const data = await response.json();
            // use the json object to update component states
            setCharacter(camelcaseKeys(data, {deep: true}));
        }
    };

    // If the url changes, reload data
    useEffect(loadData, [url]);
    return character;
}