import React, { Component } from "react";
import { render } from "react-dom";

class App extends Component {
    render() {
        return "Hello World";
    }
}

export default App;

const container = document.getElementById("learning-app");
render(<App />, container);
