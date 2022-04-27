import asyncio
from typing import Any

import async_timeout
from aioredis import Redis
from aioredis.client import PubSub
from redis import StrictRedis

from config import config


class RedisPublisher:
    """
    Class for publish message to Redis.

        * redis     - Redis client for pubsub. (StrictRedis)
        * publish   - Method for publish message to channel.
    """
    redis: StrictRedis

    def __init__(self):
        self.redis = StrictRedis(config.REDIS_HOST, charset="utf-8", decode_responses=True)

    def publish(self, name: str, message: Any) -> None:
        """
        Method for publish message to channel.

        Parameters
        ----------
        name: Target channel name
        message: Message for publish.

        Returns
        -------
        None
        """
        subs = dict(self.redis.pubsub_numsub(name))
        if subs.get(str(name), 0) > 1:
            self.redis.publish(name, message)


class RedisListener:
    """
    Class for listen messages in Redis.
    Designed for use with asynchronous code.

        * redis     - Async redis client for listening.
        * _listener - Listener messages in channel.
        * listen    - Method for run listen messages in channel.
    """

    redis: Redis

    def __init__(self):
        self.redis = Redis.from_url("redis://localhost", max_connections=10, decode_responses=True)

    @staticmethod
    async def _listener(channel: PubSub, callback, *args) -> None:
        """
        Listener messages in channel.

        Parameters
        ----------
        channel: PubSub instance
        callback: Callback for execute if detect message.
        args: Args for callback method.

        Returns
        -------
        None
        """
        while True:
            try:
                async with async_timeout.timeout(1):
                    message = await channel.get_message(ignore_subscribe_messages=True)
                    if message is not None:
                        await callback(message["data"], *args)
                    await asyncio.sleep(0.01)
            except asyncio.TimeoutError:
                pass

    async def listen(self, name, callback, *args) -> None:
        """
        Method for run liten messages in channel by name.

        Parameters
        ----------
        name: Channel name.
        callback: Callback for execute if detect message.
        args: Args for callback method.

        Returns
        -------
        None
        """
        psub = self.redis.pubsub()
        async with psub as p:
            await p.subscribe(name)
            await self._listener(p, callback, *args)
            await p.unsubscribe(name)
        await psub.close()


publisher = RedisPublisher()
listener = RedisListener()
