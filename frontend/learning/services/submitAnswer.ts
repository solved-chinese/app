import 'camelcase-keys';
import $ from 'jquery';
import AnswerVerificationResponse from '@interfaces/AnswerVerificationResponse';
import camelcaseKeys from 'camelcase-keys';

/** 
 * Check the correctness of an answer for the review question designated by
 * the question id. Return a promise of the question verification server 
 * response object. Reject the promise if the server didn't respond ok.
 */
export default function submitAnswer(qid: number, id: string, answer: string|number|[number]):
    Promise<AnswerVerificationResponse> {

    let CSRFToken = $('[name=csrfmiddlewaretoken]').val();
    return new Promise((resolve, reject) => {
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
            if (response.ok) {
                return response.json();
            } else {
                reject(`Couldn't verify the answer, response: ${response.status}`);
            }
        }).then( json => {
            resolve(camelcaseKeys(json, {deep: true}));
        });
    });
}