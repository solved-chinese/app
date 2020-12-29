import React from 'react';
import { render } from 'react-dom';
import CharDisplay from './CharDisplay.js';
import { ThemeProvider } from 'styled-components';

const theme = {
    main: '#be132d',
    primaryText: '#303545',
    secondaryText: '#5d6165',
    teritaryText: '#82878f',
    contentBackground: '#fefeff'
};
class App extends React.Component {


    render() {
        return (
            <ThemeProvider theme={theme}>
                <CharDisplay />
            </ThemeProvider>
        );
    }
}

export default App;

const container = document.getElementById('learning-app');
render(<App />, container);
