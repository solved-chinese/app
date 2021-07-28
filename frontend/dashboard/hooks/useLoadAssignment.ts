import { useState, useEffect } from "react";

import Constant from "@utils/constant";
import useLoadAssignment from "@assignment.hooks/useLoadAssignment";

/**
 * Load the assignments from URL, returns null when it is still
 * loading. The function will automatically reload the
 * returned user if the URL that's passed in changes.
 * Reattempt in 5 seconds if loading fails.
 */

/**
 * This interface Assignment is different from @interface/Assignment
 */
interface Assignment {
  name: string;
  pk: number;
  url: string;
}

const useLoadAssignments = (url: string): Assignment[] | null => {
  const [assignments, setAssignments] = useState(null);

  const loadData = async () => {
    setAssignments(null);
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
      setAssignments(data.students);
    }
  };

  // If the url changes, reload data
  useEffect(() => {
    loadData();
  }, [url]);
  return assignments;
};

export default useLoadAssignments;
