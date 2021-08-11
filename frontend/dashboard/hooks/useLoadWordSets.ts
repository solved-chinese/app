import { useState, useEffect } from "react";
import Constant from "@utils/constant";

import { SimpleWordSet } from "@interfaces/WordSet";

/**
 * Load the classes from URL, returns null when it is still
 * loading. The function will automatically reload the
 * returned user if the URL that's passed in changes.
 * Reattempt in 5 seconds if loading fails.
 */

const useLoadWordSets = (url: string): SimpleWordSet[] | null => {
  const [wordsets, setWordSets] = useState(null);

  const loadData = async () => {
    setWordSets(null);
    const response = await fetch(url);
    if (!response.ok) {
      if (response.status === 404) {
        return;
      }
      setTimeout(loadData, Constant.REQUEST_TIMEOUT);
    } else {
      // parse the response object into json
      const data = await response.json();
      console.log(data);
      // use the json object to update component states
      setWordSets(data);
    }
  };

  // If the url changes, reload data
  useEffect(() => {
    loadData();
  }, [url]);
  return wordsets;
};

export default useLoadWordSets;

export const useLoadWordSet = (url: string): SimpleWordSet | null => {
  const [wordset, setWordSet] = useState(null);

  const loadData = async () => {
    setWordSet(null);
    const response = await fetch(url);
    if (!response.ok) {
      if (response.status === 404) {
        return;
      }
      setTimeout(loadData, Constant.REQUEST_TIMEOUT);
    } else {
      // parse the response object into json
      const data = await response.json();
      console.log(data);
      // use the json object to update component states
      setWordSet(data);
    }
  };

  // If the url changes, reload data
  useEffect(() => {
    loadData();
  }, [url]);
  return wordset;
};
