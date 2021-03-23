import { useState, useEffect } from 'react';
import 'core-js/stable';
import 'regenerator-runtime/runtime';
import camelcaseKeys from 'camelcase-keys';

import { Radical } from '@interfaces/CoreItem';
import Constant from '@utils/constant';

/**
 * Load the radical from URL, returns null when it is still
 * loading. The function will automatically reload the
 * returned radical if the URL that's passed in changes. 
 * Reattempt in 5 seconds if loading fails.
 * @param {String} url 
 * 
 * @returns {Radical} The state of the loaded radical
 */
export default function useLoadRad(url) {

    const [radical, setRadical] = useState(null);
    
    const loadData = async () => {
        const response = await fetch(url);
        if (!response.ok) {
            if (response.status === 404) { return; }
            setTimeout(loadData, Constant.REQUEST_TIMEOUT);
        }

        const data = await response.json();
        setRadical(camelcaseKeys(data, {deep: true}));
    };

    // If the url changes, reload data
    useEffect(loadData, [url]);
    return radical;
}