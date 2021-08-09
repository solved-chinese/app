import { Class } from "@interfaces/Class";
import React, { ReactElement } from "react";
import styled from "styled-components";
import useLoadClasses from "../hooks/useLoadClass";

import SetDashboard from "./SetDashboard";

import Students from "./Students";
import Tabs from "./Tabs";
import "../styles/Tab.css";


const Container = styled.div`
  background-color: lightgray;
  padding: 30px;
  display: flex;
`;

const RightContainer = styled.div`
  width: 30%;
  position: relative;
`;

const LeftContainer = styled.div`
  width: 70%;
`;

type ClassesProps = {
  class: Class | null;
  classes: Class[] | null;
};

type ClassProps = {
  class: Class;
};

const ClassInfo = (props: ClassProps): JSX.Element => {
  return <div>class code : {props.class.code}</div>;
};

const Menu = (props: ClassesProps): JSX.Element => {
  if (props.class == null || props.classes == null) {
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
  return cs?.map((c, index) => (
    // console.log(c.name)
    <SetDashboard key={c.pk} index={index} class={c} />
  ));
};

const ClassDashboard = (): JSX.Element => {
  const classes = useLoadClasses("/api/classroom/teacher");

  const currentClass = classes ? classes[0] : null;

  // const students =
  //   currentClass == null
  //     ? null
  //     : useLoadStudents(
  //         `/api/classroom/class/currentclass/${currentClass?.pk}`
  //       );
  return (
    <>
      {/* <Menu class={currentClass} classes={classes} />
      <Container>
        <LeftContainer>
          
        </LeftContainer>
        <RightContainer>
          {currentClass == null ? null : <ClassInfo class={currentClass} />}
          {students == null ? null : <Students students={students} />}
        </RightContainer>
      </Container> */}
      <Tabs>
        {getClasses(classes ? classes : [])}
      </Tabs>
    </>
  );
};

export default ClassDashboard;
