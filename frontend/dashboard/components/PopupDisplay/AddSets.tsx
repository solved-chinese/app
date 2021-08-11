import Cookies from "js-cookie";
import React, { Component, SyntheticEvent, useEffect, useState } from "react";

import styled from "styled-components";
import { Class, FullClass } from "@interfaces/Class";
// import {Form, Input, Submit} from "react-nicer-inputs";
import Constant from "@utils/constant";

import { ButtonClass } from "../Title";
import useLoadWordSets, { useLoadWordSet } from "../../hooks/useLoadWordSets";
import { number } from "prop-types";

type Props = {
  className: string | undefined;

  classpk: number | undefined;
};

const SetsContainer = styled.div`
  display: block;
  position: relative;
  height: 200px;
  overflow: auto;
`;

const BottomContainer = styled.div`
  position: absolute;
  right: 5px;
  bottom: 2px;
  width: auto;
  padding: 15px;
`;

const AddSets = (props: Props): JSX.Element => {
  const className = props.className;
  const classPid = props.classpk;

  interface passSet {
    name: string;
    pid: number;
  }

  const [state, setState] = useState<passSet[]>([]);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const target = event.target;

    console.log(target);

    const name = target.name;
    const value = Number(target.value);

    if (target.checked) {
      setState([...state, { name: name, pid: value }]);
      // state.setpid[value] = value;
    } else {
      setState(state.filter((item) => item.name !== name));
    }
  };

  const wordSets = useLoadWordSets("/api/content/word_set");

  const displayWordSets = (): JSX.Element => {
    if (wordSets == null) {
      return <>No word sets</>;
    } else {
      return (
        <>
          {wordSets.map((wordset, i) => {
            return (
              <label key={i}>
                <input
                  type="checkbox"
                  name={wordset.name}
                  value={wordset.pk}
                  onChange={(e) => handleInputChange(e)}
                />
                {wordset.name}
              </label>
            );
          })}
        </>
      );
    }
  };

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
          body: JSON.stringify({
            student_ids: [],
            name: className,
            assignments: [state],
          }),
        };
      default:
        return {
          method: "PUT",
          headers: {
            "content-type": "application/json",
            "X-CSRFToken": token,
          },
          body: JSON.stringify({
            student_ids: [],
            name: className,
            assignments: [state],
          }),
        };
    }
  };

  const putData = async (url: string) => {
    const response = await fetch(url, requestOptions());
    if (!response.ok) {
      if (response.status == 404) {
        return;
      }
      setTimeout(putData, Constant.REQUEST_TIMEOUT);
    } else {
      const d = await response.json();
      console.log(d);
    }
  };

  const handleSubmit = () => {
    return putData(`/api/classroom/class/${classPid}`);
  };

  return (
    <>
      <form onSubmit={handleSubmit}>
        <SetsContainer>{displayWordSets()}</SetsContainer>
        <BottomContainer>
          <ButtonClass className="">Cancel</ButtonClass>
          <ButtonClass className={className == "" ? "disabled" : "submit"}>
            Save
          </ButtonClass>
        </BottomContainer>
      </form>
    </>
  );
};

export default AddSets;
