import { useState, useEffect } from 'react';
import 'core-js/stable';
import 'regenerator-runtime/runtime';
import 'camelcase-keys';
import ReviewQuestion from '@interfaces/ReviewQuestion';
import { async } from 'regenerator-runtime/runtime';
import camelcaseKeys from 'camelcase-keys';
import Constant from '@utils/constant';

/**
 * Return a hook to the review question provided by the URL.
 * @param {String} url 
 * @returns {ReviewQuestion | null} Review question object
 */
export default function useReviewQuestion(url) {

    const [question, setQuestion] = useState(null);

    const loadData = async () => {
        setQuestion(null);
        let response = await fetch(url);
        if (!response.ok) {
            if (response.status == 404) { return; }
            setTimeout(loadData, Constant.REQUEST_TIMEOUT);
        } else {
            let data = await response.json();
            setQuestion(camelcaseKeys(data, {deep: true}));
        }
    };

    useEffect(loadData, [url]);

    return question;
}