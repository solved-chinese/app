import Cookies from "js-cookie";
import React, { Component, SyntheticEvent, useEffect, useState } from "react";

import styled from "styled-components";
import { Class, FullClass } from "@interfaces/Class";
// import {Form, Input, Submit} from "react-nicer-inputs";
import Constant from "@utils/constant";

import { ButtonClass } from "../Title";
import useLoadWordSets, { useLoadWordSet } from "../../hooks/useLoadWordSets";
import { number } from "prop-types";
import { post } from "jquery";
import { Word } from "@interfaces/WordSet";

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

type postProps = {
  name: string;
  word_ids: number[];
  klass: number | undefined;
};

const AddSets = (props: Props): JSX.Element => {
  const className = props.className;
  const classPid = props.classpk;

  // console.log("current class is:" + className)

  interface passSet {
    name: string;
    pid: number;
  }

  const [state, setState] = useState<passSet[]>([]);

  const [assignments, setAssignments] = useState<postProps[]>([]);

  const [setIds, setSetIds] = useState<number[]>([]);

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

  /**
   * Load corresponding word sets (in state )
   */

  const loadData = (url: string) => {
    alert(url);
    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        const word_ids = data.words.map((word: Word) => word.pk);
        postData("/api/classroom/assignment", {
          name: data.name,
          word_ids: word_ids,
          klass: classPid,
        });
        // setAssignments([...assignments, {name:data.name,word_ids:word_ids,klass:className}])
      });
  };

  // If the url changes, reload data
  useEffect(() => {
    setSetIds(state.map((set) => set.pid));
  }, [state]);

  // useEffect(() => {
  //   console.log(setIds)
  //   setIds.map(id =>
  //     loadData(`/api/content/word_set/${id}`)
  //   )
  // }, [setIds])

  /**
   * Post data functions
   * @param props:postProps
   */

  const requestOptions = (props: postProps) => {
    const token = Cookies.get("csrftoken");
    switch (token) {
      case undefined:
        return {
          method: "POST",
          headers: {
            "content-type": "application/json",
            "X-CSRFToken": "",
          },
          body: JSON.stringify({
            name: props.name,
            klass: props.klass,
            word_ids: props.word_ids,
            character_ids: [],
            radicals_ids: [],
          }),
        };
      default:
        return {
          method: "POST",
          headers: {
            "content-type": "application/json",
            "X-CSRFToken": token,
          },
          body: JSON.stringify({
            name: props.name,
            klass: props.klass,
            word_ids: props.word_ids,
            character_ids: [],
            radicals_ids: [],
          }),
        };
    }
  };

  const simpleRequestOptions = (props: postProps) => {
        return {
          method: "POST",
          headers: {
            "content-type": "application/json",
          },
          body: JSON.stringify({
            name: props.name,
            klass: props.klass,
            word_ids: props.word_ids,
            character_ids: [],
            radicals_ids: [],
          }),
        };
    };

  const postData = async (url: string, props: postProps) => {
    alert(props.name);
    const assignment = props;
    fetch(url, simpleRequestOptions(assignment)).then(res => res.json()).then(data => alert(data));
  };

  // event:React.FormEvent<HTMLFormElement>
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault;

    // // Load Data works
    // setIds.forEach(id => {
    //   loadData(`/api/content/word_set/${id}`)
    // })

    postData("/api/classroom/assignment/",{name:"test2",word_ids:[],klass:classPid})
  };

  return (
    <>
      <form onSubmit={handleSubmit}>
        <SetsContainer>{displayWordSets()}</SetsContainer>
        <BottomContainer>
          <ButtonClass>Cancel</ButtonClass>
          <ButtonClass
            type={"submit"}
            className={className == undefined ? "disabled" : "submit"}
          >
            Save
          </ButtonClass>
        </BottomContainer>
      </form>
    </>
  );
};

export default AddSets;
