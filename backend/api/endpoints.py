from logging import Logger, getLogger

from fastapi import APIRouter
from fastapi import HTTPException
from starlette.websockets import WebSocket, WebSocketState
from websockets.exceptions import ConnectionClosedError

from api.schemas import TradeToolsResponse, PriceHistoryResponse
from utils.db.models import TradeTool, PriceHistory
from utils.redis import listener

ws_logger: Logger = getLogger('WSLogger')
trade_tool_router = APIRouter(prefix="/trade-tool", responses={404: {"description": "Not found"}})


@trade_tool_router.get("/", response_model=TradeToolsResponse)
def gat_trade_tools():
    """Get all trade tools."""
    return {'items': TradeTool.all()}


@trade_tool_router.get("/{trade_tool_id}/history-price", response_model=PriceHistoryResponse)
def get_price_history(trade_tool_id: int):
    """Get price history for trade tool."""
    if not TradeTool.get_by_id(target_id=trade_tool_id):
        raise HTTPException(status_code=404, detail=f"Could not found trade tool with id: {trade_tool_id}")
    return {'items': PriceHistory.get_history_prices(trade_tool_id)}


async def send_text_callback(message: str, client: WebSocket):
    """Callback for return data to ws client."""
    if client.client_state == WebSocketState.DISCONNECTED:
        ws_logger.info(f"WS client disconnected {client.client}")
        return
    await client.send_text(message)


@trade_tool_router.websocket("/{trade_tool_id}/ws")
async def websocket_endpoint(websocket: WebSocket, trade_tool_id: int):
    """Websocket"""
    await websocket.accept()
    try:
        await listener.listen(trade_tool_id, send_text_callback, websocket)
    except ConnectionClosedError:
        ws_logger.info(f"WS client disconnected {websocket.client}")
