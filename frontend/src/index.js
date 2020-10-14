import React from "react";
import ReactDom from "react-dom";
import "bootstrap/dist/css/bootstrap.css";
import { NavbarPage } from "./Base";

function Index() {
  return <NavbarPage />;
}
ReactDom.render(<Index />, document.getElementById("root"));
