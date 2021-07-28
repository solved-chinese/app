import { useState, useEffect } from "react";
import { Class } from "@interfaces/Class";

import Constant from "@utils/constant";

/**
 * Load the classes from URL, returns null when it is still
 * loading. The function will automatically reload the
 * returned user if the URL that's passed in changes.
 * Reattempt in 5 seconds if loading fails.
 */
const useLoadClasses = (url: string): Class[] | null => {
  const [classes, setClasses] = useState(null);

  const loadData = async () => {
    setClasses(null);
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
      setClasses(data.classes);
    }
  };

  // If the url changes, reload data
  useEffect(() => {
    loadData();
  }, [url]);
  return classes;
};

export default useLoadClasses;
