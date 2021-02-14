import 'core-js/stable';
import 'regenerator-runtime/runtime';
import 'camelcase-keys';
import $ from 'jquery';

import camelcaseKeys from 'camelcase-keys';

/**
 * Get the next learning action from server. The server will
 * respond with either a review question or an item to display.
 */
export default function getLearningNext(url, data) {
    var csrftoken = $('[name=csrfmiddlewaretoken]').val();
    return new Promise((resolve, reject) => {
        fetch(url, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
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
}