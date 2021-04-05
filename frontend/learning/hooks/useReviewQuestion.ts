import { useState, useEffect } from 'react';
import 'camelcase-keys';
import ReviewQuestion from '@interfaces/ReviewQuestion';
import camelcaseKeys from 'camelcase-keys';
import Constant from '@utils/constant';

/**
 * Load the review question from URL, returns null
 * when it is still loading. The function will automatically update the
 * word if the URL that's passed in changes.
 * The function will reattempt in 5 seconds if loading fails.
 */
export default function useReviewQuestion(url: string): ReviewQuestion | null {

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