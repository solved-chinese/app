import 'core-js/stable';
import 'regenerator-runtime/runtime';

import AnswerVerificationResponse from '@interfaces/AnswerVerificationResponse';

/** 
 * Check the correctness of an answer given review question designated by
 * the question id. Return a promise of the question verification server 
 * response object.
 * 
 * @param {String} id The question id
 * @param {?String|Number|[Number]} answer The pending answer
 * 
 * @returns {Promise<AnswerVerificationResponse>} Server response
 */
export default function submitAnswer(id, answer) {
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    return new Promise((resolve, reject) => {
        fetch(`/content/question/${id}`, {
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
            resolve(json);
        });
    });
}