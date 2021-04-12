import { useState, useEffect } from 'react';
import { ReviewQuestionData } from '@interfaces/ReviewQuestion';
import camelcaseKeys from 'camelcase-keys';

/**
 * Load the review question from URL, returns null
 * when it is still loading. The function will automatically update the
 * word if the URL that's passed in changes.
 */
const useReviewQuestion = (url: string, completion?: (question: ReviewQuestionData)=>void): ReviewQuestionData | null => {

    const [question, setQuestion] = useState<ReviewQuestionData | null>(null);

    const loadData = async (): Promise<ReviewQuestionData> => {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`${response.status}`);
        } else {
            const data = await response.json();
            return camelcaseKeys(data, {deep: true});
        }
    };

    useEffect( () => { loadData().then( question => {
        completion && completion(question);
        setQuestion(question);
    }).catch( (status) => {
        console.error(`Error fetching review question, server responded with status ${status}`);
    }); }, [url]);

    return question;
};

export default useReviewQuestion;
