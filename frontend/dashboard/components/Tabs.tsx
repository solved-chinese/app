import React, { ReactElement, useCallback, useEffect, useState } from "react";
import TabTitle from "./TabTitle";
import "../styles/Tab.css";
import Title from "./Title";
import useLoadUser from "../hooks/useLoadUser";
import useLoadClasses from "../hooks/useLoadClass";
import { Class } from "@interfaces/Class";
import { User } from "@interfaces/User";

type Props = {
  user: User | null;
  classes: Class[] | null;
  children: ReactElement[];
};

const Tabs = (props: Props) => {
  const [selectedTab, setSelectedTab] = useState(0);
  const children = props.children;

  const classes = props.classes;
  const user = props.user;

  const [currentClass, setCurrentClass] = useState(classes?.[selectedTab]);

  // useEffect to control the async problem
  useEffect(() => {
    setCurrentClass(classes ? classes[selectedTab] : undefined);
  }, [classes, selectedTab]);

  return (
    <div>
      <Title user={user} currentClass={currentClass} />

      <ul className="tab">
        {children.map((item, index) => (
          <TabTitle
            key={index}
            index={index}
            classname={item.props.class.name}
            setSelectedTab={setSelectedTab}
          />
        ))}
      </ul>
      {children[selectedTab]}
    </div>
  );
};

export default Tabs;
