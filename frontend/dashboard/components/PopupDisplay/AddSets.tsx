import Cookies from "js-cookie";
import React, { Component, SyntheticEvent, useEffect, useState } from "react";

import styled from "styled-components";
import { Class, FullClass } from "@interfaces/Class";
// import {Form, Input, Submit} from "react-nicer-inputs";
import Constant from "@utils/constant";

import { ButtonClass } from "../Title";
import useLoadWordSets from "frontend/dashboard/hooks/useLoadWordSets";

type Props = {
  className: string;

  classpk: number;
};

const AddSets = (props: Props): JSX.Element => {
  const className = props.className;
  const wordSets = useLoadWordSets("/api/content/word_set");

  const requestOptions = () => {
    const token = Cookies.get("csrftoken");
    switch (token) {
      case undefined:
        return {
          method: "PUT",
          headers: {
            "content-type": "application/json",
            "X-CSRFToken": "",
          },
          body: JSON.stringify({ student_ids: [], name: className }),
        };
      default:
        return {
          method: "PUT",
          headers: {
            "content-type": "application/json",
            "X-CSRFToken": token,
          },
          body: JSON.stringify({ student_ids: [], name: className }),
        };
    }
  };

  const putData = async (url: string) => {
    const response = await fetch(url, requestOptions());
    if (!response.ok) {
      if (response.status === 404) {
        return;
      }
      setTimeout(putData, Constant.REQUEST_TIMEOUT);
    } else {
      const d = await response.json();
      console.log(d);
    }
  };

  return <>{wordSets}</>;
};

export default AddSets;
