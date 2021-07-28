import { useState, useEffect } from "react";
import { User } from "@interfaces/User";

import Constant from "@utils/constant";

/**
 * Load the students from URL, returns null when it is still
 * loading. The function will automatically reload the
 * returned user if the URL that's passed in changes.
 * Reattempt in 5 seconds if loading fails.
 */

export interface Student extends User {
  display_name: string;
  pk: number;
}

const useLoadStudents = (url: string): Student[] | null => {
  const [students, setStudents] = useState(null);

  const loadData = async () => {
    setStudents(null);
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
      setStudents(data.students);
    }
  };

  // If the url changes, reload data
  useEffect(() => {
    loadData();
  }, [url]);
  return students;
};

export default useLoadStudents;
