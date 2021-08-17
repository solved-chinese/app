import { useState, useEffect } from "react";
import { Class } from "@interfaces/Class";

import Constant from "@utils/constant";

const useCreateAssignment = (url: string) => {
  const [assignmentName, SetAssignmentName] = useState("");

  // This function is called when the input changes
  const handlerChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const className = event.target.value;
    SetAssignmentName(className);
  };

  const requestOptions = {
    method: "POST",
    headers: {
      "content-type": "application/json",
    },
    body: JSON.stringify({
      name: "",
      klass: "",
      word_ids: [],
      character_ids: [],
      radicals_ids: [],
    }),
  };

  const postData = async () => {
    const response = await fetch(url, requestOptions);
    if (!response.ok) {
      if (response.status === 404) {
        return;
      }
      setTimeout(postData, Constant.REQUEST_TIMEOUT);
    } else {
      const d = await response.json();
      // console.log(d);
      SetAssignmentName(d.name);
    }
  };

  return postData();

  // TODO
  // useEffect(() => {
  //     console.log("effect")
  //     createClass (url)
  // }, [className])
};
