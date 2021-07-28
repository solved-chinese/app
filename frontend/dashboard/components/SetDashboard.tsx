import { string } from "prop-types";
import React from "react";
import styled from "styled-components";

import "../styles/DashboardBody.css";

const Row = styled.div`
  height: 100px;
`;

type wordset = string; // temporary defintion

type SetProps = {
  set: wordset;
};

const SetCard = (props: SetProps): JSX.Element => {
  return <div>{props.set}</div>;
};

type Props = {
  classname: string;
  sets: wordset[];
};

const SetCards = (props: Props): JSX.Element => {
  return (
    <Row>
      <div className="smallgraytitle"></div>
      {props.sets.map((set, i) => {
        return <SetCard key={i} set={set} />;
      })}
    </Row>
  );
};

const SetDashboard = (): JSX.Element => {
  return (
    <>
      <SetCards classname="class 1" sets={["set1", "set2"]} />
    </>
  );
};

export default SetDashboard;
