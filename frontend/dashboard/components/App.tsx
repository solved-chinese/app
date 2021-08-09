import useLoadWord from "@learning.hooks/useLoadWord";
import React from "react";
import useLoadClasses from "../hooks/useLoadClass";
import ClassDashboard from "./ClassDashboard";
import SetDashboard from "./SetDashboard";
import Tabs from "./Tabs";
import Title from "./Title";

// type Props = {
//   action: string;
//   content: { qid: number };
// };

export default class App extends React.Component {
  render(): JSX.Element {
    return (
      <>
        <Title />
        <ClassDashboard />
      </>
    );
  }
}
