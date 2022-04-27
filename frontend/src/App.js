import React, {Component} from "react";
import MyChart from "./Chart";


export default class App extends Component {

    render() {
        return (
            <div className="App">
                <MyChart {...this.props}/>
            </div>
        )
    }
}
