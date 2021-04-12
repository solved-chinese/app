import { useState, useEffect } from 'react';
import camelcaseKeys from 'camelcase-keys';

import { Word } from '@interfaces/CoreItem';
import Constant from '@utils/constant';

/**
 * Load the word from URL, returns null when it is still
 * loading. The function will automatically reload the
 * returned word if the URL that's passed in changes. 
 * Reattempt in 5 seconds if loading fails.
 */
const useLoadWord = (url: string): Word | null => {

    const [word, setWord] = useState(null);

    const loadData = async () => {
        setWord(null);
        const response = await fetch(url);
        if (!response.ok) {
            if (response.status === 404) { return; }
            setTimeout(loadData, Constant.REQUEST_TIMEOUT);
        }

        // parse the response object into json
        const data = await response.json();
        // use the json object to update component states
        setWord(camelcaseKeys(data, {deep: true}));
    };

    useEffect(() => { loadData(); }, [url]);
    return word;
};

export default useLoadWord;
