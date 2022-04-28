import API from "../Api";
import WsClient from "../WsClient";

const api = new API()
const ws_client = new WsClient();

let store = {
    _state: {
        ws_client: ws_client,
        active_trade_tool: {id: 1, name: 'My'},
        all_trade_tools: [],
        new_price: null,
        history: []
    },
    getState() {
        return this._state
    },
    subscribe(observer) {
        this.rerenderApp = observer
        console.log('subscribed.')

    },
    rerenderApp() {
        console.log('State changed.')
    },
    saveHistory(history) {
        this._state.history = history.items
        this.rerenderApp(this._state)
    },
    saveAllTradeTools(all_trade_tools) {
        this._state.all_trade_tools = all_trade_tools.items
        this.rerenderApp(this._state)
    },
    changeActiveTradeTool(trade_tool_id, trade_tool_name) {
        this._state.active_trade_tool = {id: trade_tool_id, name: trade_tool_name}
        api.get_history(this._state.active_trade_tool.id).then(history => this.saveHistory(history))
        ws_client.disconnect()
        ws_client.connect(this._state.active_trade_tool.id)
        this.rerenderApp(this._state)
    }
}
ws_client.connect(store._state.active_trade_tool.id)
api.get_history(store._state.active_trade_tool.id).then(history => store.saveHistory(history))
api.get_all_trade_tools().then(all_trade_tools => store.saveAllTradeTools(all_trade_tools))

export default store;