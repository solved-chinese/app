import { Class } from "@interfaces/Class";
import React, { ReactElement, useEffect, useState } from "react";
import styled from "styled-components";
import useLoadClasses from "../hooks/useLoadClass";

import SetDashboard from "./SetDashboard";

import Students from "./Students";
import Tabs from "./Tabs";
import "../styles/Tab.css";
import Title from "./Title";
import { User } from "@interfaces/User";
import useLoadUser from "../hooks/useLoadUser";

type ClassesProps = {
  user: User | null;
  classes: Class[] | null;
};

type ClassProps = {
  class: Class;
};

const Menu = (props: ClassesProps): JSX.Element => {
  if (props.classes == null) {
    return <>There is no class</>;
  } else {
    return (
      <>
        {props.classes.map((c, i) => {
          return <a key={i}>c</a>;
        })}
      </>
    );
  }
};

const getClasses = (cs: Class[]): ReactElement[] => {
  return cs.map((c, index) => (
    // console.log(c.name)
    <SetDashboard key={c.pk} index={index} class={c} />
  ));
};

const ClassDashboard = (): JSX.Element => {
  // const classes = useLoadClasses("/api/classroom/teacher");

  // const classes = props.classes;
  // const user = props.user;
  // const currentClass = classes?.[0]

  // is Teacher ? is Student ?
  const user = useLoadUser("/api/accounts/user");

  const classes = useLoadClasses("/api/classroom/teacher");

  // useEffect(() => {
  //   setCurrentClass(classes? classes[index]: undefined)
  // }, [index])

  return (
    <>
      {/* <Title user={user} currentClass={currentClass}/> */}
      <Tabs user={user} classes={classes}>
        {getClasses(classes ? classes : [])}
      </Tabs>
    </>
  );
};

export default ClassDashboard;
