import React, {Component} from "react";
import MyChart from "./Chart";
import Select from "react-select";


export default class App extends Component {
    constructor(props) {
        super(props);
        this.state = props.state
        this.store = props.store
    }

    onChangeCallback = (event) => {
        this.store.changeActiveTradeTool(event.value, event.label)
    }

    render() {
        let options = this.state.all_trade_tools.map(function (e) {
            return {value: e.id, label: e.name}
        })
        return (
            <div className="App">
                <Select options={options} onChange={this.onChangeCallback}/>
                <MyChart {...this.props}/>
            </div>
        )
    }
}
