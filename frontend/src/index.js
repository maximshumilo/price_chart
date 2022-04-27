import React from 'react';
import App from './App';
import store from "./redux/State";

import ReactDOM from "react-dom/client";


let rerenderApp = (state) => {
    const root = ReactDOM.createRoot(document.getElementById("root"));
    root.render(
        <React.StrictMode>
            <App state={state} store={store}/>
        </React.StrictMode>
    );
}

rerenderApp(store.getState())

store.subscribe(rerenderApp)