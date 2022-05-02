class WsClient {
    set_on_message = (callback) => {
        this.onMessage = callback
    }

    disconnect = () => {
        if (this.ws != null) {
            this.ws.close()
        }
    }

    connect = (trade_tool_id) => {
        const url = (process.env.NODE_ENV === "development" ? `ws://localhost:5000/trade-tool/${trade_tool_id}/ws` : `ws://localhost:80/trade-tool/${trade_tool_id}/ws`)
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
