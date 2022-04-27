import logging

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d %(name)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class Config(BaseSettings):
    DATABASE_URL: str = Field("postgresql://root:root@postgres/prices", env='DATABASE_URL')
    REDIS_HOST: str = Field("redis", env='REDIS_HOST')


config = Config()
