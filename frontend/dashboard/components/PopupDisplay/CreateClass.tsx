import React, { Component, SyntheticEvent, useEffect, useState } from "react";

import styled from "styled-components";
import { Class, FullClass } from "@interfaces/Class";
// import {Form, Input, Submit} from "react-nicer-inputs";
import Constant from "@utils/constant";

import { ButtonClass } from "../Title";

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

  const createClass = (url: string) => {
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

    // // TODO
    // useEffect(() => {
    //     console.log("effect")
    //     createClass (url)
    // }, [className])
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
      {/* <input type="text" className="no-outline" placeholder="Enter the Class name" value={className} onChange={handlerChange}/> */}
      {/* textarea */}
      <BottomContainer>
        <ButtonClass onClick={() => SetClassName("")}> Cancel </ButtonClass>
        <ButtonClass
          className={className == "" ? "disabled" : ""}
          onClick={() => createClass("/api/classroom/class/")}
        >
          {" "}
          Save{" "}
        </ButtonClass>
      </BottomContainer>
    </>
  );
};

export default CreateClass;
