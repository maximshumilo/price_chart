from asyncio import sleep

from fastapi import APIRouter
from fastapi import HTTPException
from starlette.websockets import WebSocket
from websockets.exceptions import ConnectionClosedOK

from utils.db.models import TradeTool, PriceHistory
from utils.redis import listener

trade_tool_router = APIRouter(prefix="/trade-tool", responses={404: {"description": "Not found"}})


@trade_tool_router.get("/")
def gat_trade_tools():
    """Get all trade tools."""
    return TradeTool.all()


@trade_tool_router.get("/{trade_tool_id}/history-price")
def get_price_history(trade_tool_id: int):
    """Get price history for trade tool."""
    if not TradeTool.get_by_id(target_id=trade_tool_id):
        raise HTTPException(status_code=404, detail=f"Could not found trade tool with id: {trade_tool_id}")
    return PriceHistory.get_history_prices(trade_tool_id)


async def send_text_callback(message: str, client: WebSocket):
    """Callback for return data to ws client."""
    await client.send_text(message)


@trade_tool_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, trade_tool_id: int):
    """Websocket"""
    await websocket.accept()
    while True:
        try:
            await listener.listen(trade_tool_id, send_text_callback, websocket)
        except ConnectionClosedOK:
            print(f'Closed {websocket.client.port}')
        await sleep(1)
