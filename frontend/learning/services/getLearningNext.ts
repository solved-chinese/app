import $ from 'jquery';
import camelcaseKeys from 'camelcase-keys';
import {AnswerSubmitResponse, LearningNextResponse} from '@interfaces/CoreLearning';
import {ReviewQuestionAnswer} from '@interfaces/ReviewQuestion';

type LearningData = {
    state?: string,
    answer?: ReviewQuestionAnswer,
    stats?: {
        duration: number
    }
}

/**
 * Get the next learning action from server. The server will
 * respond with either a review question or an item to display.
 */
const getLearningNext = (url: string, data: LearningData): Promise<LearningNextResponse | AnswerSubmitResponse> => {
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
            if (response.ok && response.status == 200) {
                return response.json();
            } else {
                reject(`Get learning next: server communication error, 
                unexpected response: ${response.status}`);
            }
        }).then( json => {
            resolve(camelcaseKeys(json, {deep: true}));
        }).catch( error => {
            reject(error);
        });
    });
};

export default getLearningNext;
