import $ from 'jquery';
import camelcaseKeys from 'camelcase-keys';
import {ReviewQuestionAnswer, AnswerVerificationResponse} from '@interfaces/ReviewQuestion';

/** 
 * Check the correctness of an answer for the review question designated by
 * the question id. Return a promise of the question verification server 
 * response object. Reject the promise if the server didn't respond ok.
 */
const submitAnswer = (qid: number, id: string, answer: ReviewQuestionAnswer, completion: ()=>void):
    Promise<[AnswerVerificationResponse, ()=>void]> => {

    const CSRFToken = `${$('[name=csrfmiddlewaretoken]').val()}`;
    return new Promise<[AnswerVerificationResponse, ()=>void]>((resolve, reject) => {
        fetch(`/content/question/${qid}`, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': CSRFToken
            },
            body: JSON.stringify({
                'id': id,
                'answer': answer
            })
        }).then( response => {
            if (response.ok && response.status == 200) {
                return response.json();
            } else {
                reject(`Answer verification: server communication error, 
                unexpected response: ${response.status}`);
            }
        }).then( json => {
            resolve([camelcaseKeys(json, {deep: true}), completion]);
        }).catch( error => {
            reject(error);
        });
    });
};

export default submitAnswer;
