from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class ItemsResponseMixin(BaseModel):

    def __init__(self, **kwargs):
        kwargs['items'] = [item.__dict__ for item in kwargs['items']]
        super().__init__(**kwargs)


class TradeTool(BaseModel):
    _id: int = Field(alias='id')
    name: str
    last_price: int
    last_update_price: datetime


class TradeToolsResponse(ItemsResponseMixin):
    items: List[TradeTool]


class PriceHistory(BaseModel):
    x: int
    y: int


class PriceHistoryResponse(ItemsResponseMixin):
    items: List[TradeTool]
