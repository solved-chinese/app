import Cookies from "js-cookie";
import React, { Component, SyntheticEvent, useEffect, useState } from "react";

import styled from "styled-components";
import { Class, FullClass } from "@interfaces/Class";
// import {Form, Input, Submit} from "react-nicer-inputs";
import Constant from "@utils/constant";

import { ButtonClass } from "../Title";
import useLoadWordSets from "frontend/dashboard/hooks/useLoadWordSets";

const Input = styled.input`
  border-top-style: hidden;
  border-right-style: hidden;
  border-left-style: hidden;
  border-bottom-style: groove;
  background-color: #f1f1f196;
  border-block-color: #f1f1f196;

  width: 100%;

  &.no-outline:focus {
    outline: none;
  }
`;

const BottomContainer = styled.div`
  position: absolute;
  right: 5px;
  bottom: 2px;
  width: auto;
  padding: 15px;
`;

const CreateClass = (): JSX.Element => {
  const [className, SetClassName] = useState("");

  // This function is called when the input changes
  const handlerChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const className = event.target.value;
    SetClassName(className);
  };

  const requestOptions = () => {
    const token = Cookies.get("csrftoken");
    switch (token) {
      case undefined:
        return {
          method: "POST",
          headers: {
            "content-type": "application/json",
            "X-CSRFToken": "",
          },
          body: JSON.stringify({ student_ids: [], name: className }),
        };
      default:
        return {
          method: "POST",
          headers: {
            "content-type": "application/json",
            "X-CSRFToken": token,
          },
          body: JSON.stringify({ student_ids: [], name: className }),
        };
    }
  };

  // const requestOptions = {
  //   method: "POST",
  //   headers: {
  //     "content-type": "application/json",
  //     "X-CSRFToken": Cookies.get('csrftoken'),
  //   },
  //   body: JSON.stringify({ student_ids: [], name: className }),
  // };

  const postData = async (url: string) => {
    const response = await fetch(url, requestOptions());
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

  return (
    <>
      <Input
        type="text"
        className="no-outline"
        placeholder="Enter the Class name"
        value={className}
        onChange={handlerChange}
      />
      <a>Class Name</a>
      {/* <div>
        {wordSets}
      </div> */}
      <BottomContainer>
        <ButtonClass onClick={() => SetClassName("")}> Cancel </ButtonClass>
        <ButtonClass
          className={className == "" ? "disabled" : ""}
          onClick={() => {
            postData("/api/classroom/class/");
            SetClassName("");
          }}
        >
          {" "}
          Save{" "}
        </ButtonClass>
      </BottomContainer>
    </>
  );
};

export default CreateClass;
