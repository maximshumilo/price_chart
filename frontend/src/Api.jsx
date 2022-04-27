import Axios from 'axios';

export default class API {
    constructor() {
        const base_url = (process.env.NODE_ENV === "development" ? 'http://0.0.0.0:5000' : '/')
        this.axios = Axios.create({baseURL: base_url});
    }

    async get_history(trade_tool_id) {
        const response = await this.axios.get(`/trade-tool/${trade_tool_id}/history-price`)
            .catch((error) => {
                throw error
            })
        return response.data
    }

}