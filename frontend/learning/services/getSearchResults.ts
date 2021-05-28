import $ from 'jquery';
import camelcaseKeys from 'camelcase-keys';
import { SearchResult, SearchParams } from '@interfaces/Search';

/**
 * Get the next learning action from server. The server will
 * respond with either a review question or an item to display.
 */
const getSearchResults = (searchParams: SearchParams): Promise<SearchResult> => {
    const CSRFToken = $('[name=csrfmiddlewaretoken]').val() as string;
    return new Promise((resolve, reject) => {
        fetch('/content/search_api/', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': CSRFToken
            },
            body: JSON.stringify({...searchParams})
        }).then( response => {
            if (response.ok && response.status == 200) {
                return response.json();
            } else {
                reject(`Search: server communication error, 
                unexpected response: ${response.status}`);
            }
        }).then( json => {
            resolve(camelcaseKeys(json, {deep: true}));
        }).catch( error => {
            reject(error);
        });
    });
};

export default getSearchResults;
