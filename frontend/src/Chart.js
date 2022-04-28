import 'chartjs-adapter-luxon';
import React, {Component} from "react";
import {TimeScale} from 'chart.js';
import {Line} from "react-chartjs-2";
import Chart from "chart.js/auto";

import WsClient from "./WsClient";

Chart.register(TimeScale);


class MyChart extends Component {
    constructor(props) {
        super(props);
        this.chartReference = React.createRef();
        this.state = props.state

        const onMessage = (event) => {
            const message = JSON.parse(event.data)
            const chart = this.chartReference.current;
            if (chart != null) {
                chart.data.datasets[0].data.push(message)
                chart.update();
            }
        }
        this.state.ws_client.set_on_message(onMessage)

        // new WsClient(onMessage, this.state);
    }

    render() {
        const data = {
            datasets: [{
                label: this.state.active_trade_tool.name,
                fill: false,
                lineTension: 0,
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgba(255, 99, 132, 0.5)',
                borderDash: [8, 4],
                data: this.state.history
            }]
        }
        const options = {
            animation: {
                duration: 0
            },
            scales: {
                xAxes: {
                    type: 'time'
                }
            }
        }
        return (
            <Line ref={this.chartReference} data={data} options={options}/>
        )
    }
}

export default MyChart;