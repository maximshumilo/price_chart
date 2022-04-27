class WsClient {
    constructor(onMessage) {
        this.onMessage = onMessage
        this.connect()
    }

    connect = () => {
        this.ws = new WebSocket('ws://localhost:80/trade-tool/1/ws')

        this.ws.onopen = () => {
            console.log('connected')
        }

        this.ws.onmessage = evt => {
            this.onMessage(evt)
        }

        this.ws.onclose = () => {
            console.log('disconnected')
        }
    }
}

export default WsClient;
