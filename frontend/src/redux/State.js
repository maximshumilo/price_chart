import API from "../Api";

const api = new API()

let store = {
    _state: {
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
}
api.get_history(1).then(history => store.saveHistory(history))

export default store;