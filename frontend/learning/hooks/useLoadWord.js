import { useState, useEffect } from 'react';
import 'core-js/stable';
import 'regenerator-runtime/runtime';
import camelcaseKeys from 'camelcase-keys';
import { async } from 'regenerator-runtime/runtime';

import { Word } from '@interfaces/CoreItem';

/**
 * Load the word from URL, returns null when it is still
 * loading. The function will automatically reload the
 * returned word if the URL that's passed in changes. 
 * Reattempt in 5 seconds if loading fails.
 * @param {String} url 
 * 
 * @returns {Word}
 */
export default function useLoadWord(url) {

    const [word, setWord] = useState(null);

    const loadData = async () => {
        const response = await fetch(url);
        if (!response.ok) {
            if (response.status === 404) { return; }
            setTimeout(loadData, 5000);
        }

        // parse the response object into json
        const data = await response.json();
        // use the json object to update component states
        setWord(camelcaseKeys(data, {deep: true}));
    };

    useEffect(loadData, [url]);
    return word;
}