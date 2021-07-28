import React from "react";
import styled from "styled-components";
import { Student } from "../hooks/useLoadStuents";

import "../styles/DashboardBody.css";

type StuProps = {
  students: Student[];
};

type Props = {
  student: Student;
};

const StudentCard = (props: Props): JSX.Element => {
  return <>{props.student}</>;
};

const Students = (props: StuProps): JSX.Element => {
  return (
    <div>
      {props.students.map((student, i) => {
        return <StudentCard student={student} key={i} />;
      })}
    </div>
  );
};

export default Students;
