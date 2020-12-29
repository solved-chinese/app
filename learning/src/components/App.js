import React, { Component } from "react";
import { render } from "react-dom";
import WordDefinition from "./WordDefinition";
import ExampleSentences from './ExampleSentences'

class App extends Component {
    render() {
        //change the following constants with actual data
        const cn = "字";
        const py = "zi";
        const src = "here";
        const arr = [
            {
                "part_of_speech": "n.",
                "definition"    : "a noun \n second line"
            },
            {
                "part_of_speech": "adj.",
                "definition"    : "an adj"
            }];

        return (
            <div>
                <WordDefinition
                    word={cn}
                    pinin={py}
                    audiosrc={src}
                    definitions={arr}
                />
                {/* Example Sentences */}
                <h1 className='exampleTitle'>Example Sentences</h1>
                <ExampleSentences/>
            </div>
        );
    }
}

export default App;

const container = document.getElementById("learning-app");
render(<App />, container);