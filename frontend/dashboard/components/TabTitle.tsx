import React, { useCallback } from "react";
import "../styles/Tab.css";

type Props = {
  classname: string;
  index: number;
  setSelectedTab: (index: number) => void;
};

// const TabTitle : React.FC<Props> = ({classname}) => {
//     return (
//         <li>
//             <button>{classname}</button>
//         </li>
//     )
// }

const TabTitle = (props: Props) => {
  const onClick = useCallback(() => {
    props.setSelectedTab(props.index);
  }, [props.setSelectedTab, props.index]);

  console.log(props.classname);

  return (
    <li>
      <button className="tab-title" onClick={onClick}>{props.classname}</button>
    </li>
  );
};

export default TabTitle;
