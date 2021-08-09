import { string } from "prop-types";
import React from "react";
import styled from "styled-components";
import PropTypes from "prop-types";

import "../styles/DashboardBody.css";
import useLoadClasses from "../hooks/useLoadClass";
import { Class } from "@interfaces/Class";

const Row = styled.div`
  height: 100px;
`;

type wordset = string; // temporary defintion

type SetProps = {
  set: wordset;
  activeTab: boolean;
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
        return <SetCard key={i} set={set} activeTab={false} />;
      })}
    </Row>
  );
};

type TabProps = {
  class: Class;
  index: number;
};

// a container for tab content that it gets like a child

// const SetDashboard: React.FC<TabProps> = ({ children }) => {
//   return <div>{children}</div>
// }

const SetDashboard = (props: TabProps) => {
  return (
    <>
      <SetCards classname={props.class.name} sets={[]} />
    </>
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
