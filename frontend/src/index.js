import React from 'react';
import App from './App';
import store from "./redux/State";

import ReactDOM from "react-dom/client";

const root = ReactDOM.createRoot(document.getElementById("root"));

let rerenderApp = (state) => {
    root.render(
        <React.StrictMode>
            <App state={state} store={store}/>
        </React.StrictMode>
    );
}

rerenderApp(store.getState())

store.subscribe(rerenderApp)