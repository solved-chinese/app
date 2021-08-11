import { string } from "prop-types";
import React from "react";
import styled from "styled-components";
import PropTypes from "prop-types";

import "../styles/DashboardBody.css";
import useLoadClasses, { useLoadClass } from "../hooks/useLoadClass";
import { Class } from "@interfaces/Class";
import { useLoadWordSet } from "../hooks/useLoadWordSets";
import { SimpleWordSet } from "@interfaces/WordSet";
import Students from "./Students";
import useLoadStudents from "../hooks/useLoadStuents";

const Row = styled.div`
  height: 100px;
`;

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

type SetProps = {
  set: SimpleWordSet;
};

type Props = {
  classname: string;

  classpid: number;
};

type ClassProps = {
  class: Class;
  index?: number;
};

const SetCard = (props: SetProps): JSX.Element => {
  return <div>{props.set}</div>;
};

const SetCards = (props: Props): JSX.Element => {
  const classname = props.classname;

  const classpid = props.classpid;

  const klass = useLoadClass(`/api/classroom/class/${classpid}`);

  const assignments = klass?.assignements;

  // const getWordSets = () => {
  //   // the assignments here are actually word sets
  //   const assignments = klass?.assignements

  //   // const wordset = useLoadWordSet(`/api/content/word_set/${pid}`);
  //   // console.log("word set is:" + {wordset});
  //   return assignments ? assignments : null
  // }

  return (
    <Row>
      <div className="smallgraytitle"></div>

      {assignments == undefined
        ? ""
        : assignments.map((wordset, i) => {
            return <SetCard key={i} set={wordset} />;
          })}
    </Row>
  );
};

// a container for tab content that it gets like a child

// const SetDashboard: React.FC<TabProps> = ({ children }) => {
//   return <div>{children}</div>
// }

const ClassInfo = (props: ClassProps): JSX.Element => {
  return <div>class code : {props.class.code}</div>;
};

const SetDashboard = (props: ClassProps) => {
  const students = useLoadStudents(`/api/classroom/class/${props.class.pk}`);

  return (
    <Container>
      <LeftContainer>
        <SetCards classname={props.class.name} classpid={props.class.pk} />
      </LeftContainer>
      <RightContainer>
        <ClassInfo class={props.class} />
        {students == null ? null : <Students students={students} />}
      </RightContainer>
    </Container>
  );
};

export default SetDashboard;

// <div className="tabs">
// <ol className="tab-list">
//   {this.props.children.map((child) => {
//     const { label } = child.props;

//     return (
//       <Tab
//         activeTab={activeTab}
//         key={label}
//         label={label}
//         onClick={onClickTabItem}
//       />
//     );
//   })}
// </ol>
// <div className="tab-content">
//   {}
//   {children.map((child) => {
//     if (child.props.label !== activeTab) return undefined;
//     return child.props.children;
//   })}
// </div>
// </div>
