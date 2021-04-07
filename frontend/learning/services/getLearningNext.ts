import $ from 'jquery';
import camelcaseKeys from 'camelcase-keys';
import {LearningNextResponse} from '@interfaces/CoreLearning';

type LearningData = {
    state?: string,
    answer?: string,
    stats?: {
        duration?: number
    }
}

/**
 * Get the next learning action from server. The server will
 * respond with either a review question or an item to display.
 */
const getLearningNext = (url: string, data: LearningData): Promise<LearningNextResponse> => {
    const CSRFToken = $('[name=csrfmiddlewaretoken]').val() as string;
    return new Promise((resolve, reject) => {
        fetch(url, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': CSRFToken
            },
            body: JSON.stringify({...data})
        }).then( response => {
            if (response.ok) {
                return response.json();
            } else {
                reject(`error: ${response.status}`);
            }
        }).then( json => {
            resolve(camelcaseKeys(json, {deep: true}));
        });
    });
};

export default getLearningNext;
