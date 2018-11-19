import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import AppContainer from './AppContainer';
import registerServiceWorker from './registerServiceWorker';

let el =  document.getElementById('root');
ReactDOM.render(<AppContainer />, el);
registerServiceWorker();