import { Class } from "@interfaces/Class";
import { User } from "@interfaces/User";
import useLoadWord from "@learning.hooks/useLoadWord";
import { timers } from "jquery";
import React, { useState } from "react";
import useLoadClasses from "../hooks/useLoadClass";
import useLoadUser from "../hooks/useLoadUser";
import ClassDashboard from "./ClassDashboard";
import SetDashboard from "./SetDashboard";
import Tabs from "./Tabs";
import Title from "./Title";

// type Props = {
//   user : User | null;
//   classes : Class [] | null;
// }

const Dashboard = (): JSX.Element => {
  return (
    <>
      <ClassDashboard />
    </>
  );
};

export default class App extends React.Component {
  // constructor (props: {} ) {
  //   super(props);
  //   this.state = {
  //     user : useLoadUser("/api/accounts/user"),
  //     classes : useLoadClasses("/api/classroom/teacher"),
  //     currentclass : useLoadClasses("/api/classroom/teacher")?.[0]
  //   }
  // }

  render(): JSX.Element {
    return <Dashboard />;
  }
}
