import React, { ReactElement, useState } from "react";
import TabTitle from "./TabTitle";
import "../styles/Tab.css";


type Props = {
  children: ReactElement[];
};

const Tabs = (props: Props) => {
  const [selectedTab, setSelectedTab] = useState(0);
  const children = props.children;

  return (
    <div>
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
