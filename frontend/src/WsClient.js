class WsClient {
    constructor(onMessage) {
        this.onMessage = onMessage
        this.connect()
    }

    connect = () => {
        const url = (process.env.NODE_ENV === "development" ? 'ws://localhost:5000/trade-tool/1/ws' : 'ws://localhost:80/trade-tool/1/ws')
        this.ws = new WebSocket(url)

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
