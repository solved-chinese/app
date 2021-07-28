import { useState, useEffect } from "react";
import { Class } from "@interfaces/Class";

import Constant from "@utils/constant";



const useCreateClass = (url: string) => {

    const [className, SetClassName] = useState("");

    // This function is called when the input changes
    const handlerChange = (event: React.ChangeEvent<HTMLInputElement>) => {
      const className = event.target.value;
      SetClassName(className);
    };
  
    const requestOptions = {
      method: "POST",
      headers: {
        "content-type": "application/json",
      },
      body: JSON.stringify({ student_ids: [], name: className }),
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
        console.log(d);
      }
    };

    return postData();

    // TODO
    // useEffect(() => {
    //     console.log("effect")
    //     createClass (url)
    // }, [className])
  };