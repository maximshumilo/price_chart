import json
from datetime import datetime
from random import random
from time import sleep
from typing import List

from utils.db.models import TradeTool, PriceHistory
from utils.redis import publisher
from .base_model import Task


class PriceMovement(Task):
    """
    Task for prices movement.

    First, data on the latest prices are loaded from the database, then prices change in a cycle 1 time per second.

        * _load_last_prices             - Load last prices from DB to memory.
        * _generate_movement            - Generates the step of the price change.
        * _generate_new_prices_info     - Generates a list of updated prices.
        * _update_price                 - Update prices in DB.
        * _start                        - Entrypoint for start task.
    """
    _last_prices: dict

    def _load_last_prices(self) -> None:
        """Load last prices from DB to memory."""
        self._last_prices = {tool.id: tool.last_price for tool in TradeTool.all()}

    @staticmethod
    def _generate_movement() -> int:
        """Generates the step of the price change."""
        movement = -1 if random() < 0.5 else 1
        return movement

    def _generate_new_prices_info(self) -> List[tuple]:
        """
        Generates a list of updated prices.
        And also, when generating a new price for the instrument, it is immediately published in redis.
        """
        new_prices_info = []
        for tool_id, price in self._last_prices.items():
            updated_time = datetime.now()
            price += self._generate_movement()
            new_prices_info.append((tool_id, price, updated_time))
            self._last_prices[tool_id] = price
            publisher.publish(name=tool_id, message=json.dumps({"y": price, "x": int(updated_time.timestamp())}))
        return new_prices_info

    def _update_price(self) -> None:
        """Update prices in DB"""
        new_prices_info = self._generate_new_prices_info()
        TradeTool.update_batch(new_prices_info)
        PriceHistory.create_batch(new_prices_info)

    def _start(self) -> None:
        """Entrypoint for start task."""
        self._load_last_prices()
        while True:
            self._update_price()
            sleep(1)
            self._logger.debug('Task is running. Successfully updated prices.')
