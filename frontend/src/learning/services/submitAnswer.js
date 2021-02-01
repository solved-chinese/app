import 'core-js/stable';
import 'regenerator-runtime/runtime';
import 'camelcase-keys';
import $ from 'jquery';

import AnswerVerificationResponse from '@interfaces/AnswerVerificationResponse';
import camelcaseKeys from 'camelcase-keys';

/** 
 * Check the correctness of an answer given review question designated by
 * the question id. Return a promise of the question verification server 
 * response object.
 * 
 * @param {Number} qid The question's query id
 * @param {String} id The question id
 * @param {?String|Number|[Number]} answer The pending answer
 * 
 * @returns {Promise<AnswerVerificationResponse>} Server response
 */
export default function submitAnswer(qid, id, answer) {
    var csrftoken = $('[name=csrfmiddlewaretoken]').val();
    return new Promise((resolve, reject) => {
        fetch(`/content/question/${qid}`, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
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