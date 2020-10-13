import React from "react";
import ReactDom from "react-dom";
import "bootstrap/dist/css/bootstrap.css";

function Base() {
  return <h4>HelloWorld</h4>;
}

ReactDom.render(<Base />, document.getElementById("root"));
