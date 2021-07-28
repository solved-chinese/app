import { useState, useEffect } from "react";
import { User } from "@interfaces/User";

import Constant from "@utils/constant";

/**
 * Load a user from URL, returns null when it is still
 * loading. The function will automatically reload the
 * returned user if the URL that's passed in changes.
 * Reattempt in 5 seconds if loading fails.
 */
const useLoadUser = (url: string): User | null => {
  const [user, setUser] = useState(null);

  const loadData = async () => {
    setUser(null);
    const response = await fetch(url);
    if (!response.ok) {
      if (response.status === 404) {
        return;
      }
      setTimeout(loadData, Constant.REQUEST_TIMEOUT);
    } else {
      // parse the response object into json
      const data = await response.json();
      // use the json object to update component states
      setUser(data);
    }
  };

  // If the url changes, reload data
  useEffect(() => {
    loadData();
  }, [url]);
  return user;
};

export default useLoadUser;
