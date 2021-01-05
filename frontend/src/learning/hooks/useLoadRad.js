import React, { useState, useEffect } from 'react';
import 'core-js/stable';
import 'regenerator-runtime/runtime';

/**
 * Load the radical from URL, returns null when it is still
 * loading.
 * @param {String} url 
 */
export default function useLoadRad(url) {

    const [radical, setRadical] = useState(null);
    
    const loadData = async () => {
        const response = await fetch(url);
        if (!response.ok) {
            setTimeout(() => {
                this.loadData();
            }, 5);
        }

        const data = await response.json();
        setRadical(data);
    };

    // If the url changes, reload data
    useEffect(loadData, [url]);
    return radical;
}
