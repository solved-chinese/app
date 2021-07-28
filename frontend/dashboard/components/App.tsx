import useLoadWord from "@learning.hooks/useLoadWord";
import React from "react";
import useLoadClasses from "../hooks/useLoadClass";
import ClassDashboard from "./ClassDashboard";
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
