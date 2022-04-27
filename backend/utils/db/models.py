from datetime import datetime
from typing import List

from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship

from .db import BaseModelMixin, Base, engine


class TradeTool(Base, BaseModelMixin):
    """
    Model of trade tool.

        * __tablename__     - Table name in db
        * name              - tool name
        * last_price        - Last price
        * last_update_price - Last update price
        * price_history     - Instances of model PriceHistory
    """
    __tablename__ = "trade_tool"

    name = Column(String, unique=True)
    last_price = Column(Integer)
    last_update_price = Column(TIMESTAMP)
    history_prices = relationship("PriceHistory", back_populates="trade_tool")

    @classmethod
    def create(cls, **kwargs) -> "Base":
        """
        Create new TradeTool.
        Set current datetime to `last_update_price`.

        Parameters
        ----------
        kwargs: Data

        Returns
        -------
        Instance
        """
        kwargs['last_update_price'] = datetime.now()
        return super().create(**kwargs)

    @classmethod
    def update_batch(cls, update_data: List[tuple]) -> None:
        """
        Update last_price for multiply rows

        Parameters
        ----------
        update_data: List of tuple. [ID, last_price, last_update_price), ...]

        Returns
        -------
        None
        """
        target_update = ', '.join([f"({_id}, {price}, '{date}'::timestamp)" for _id, price, date in update_data])
        sql_raw = f"""
        UPDATE trade_tool AS m
        SET last_price = c.last_price,
            last_update_price = c.last_update_price
        FROM (values {target_update}) AS c(id, last_price, last_update_price)
        WHERE c.id = m.id
        """
        cls._manager.execute_sql(raw=sql_raw)


class PriceHistory(Base, BaseModelMixin):
    """
    Model history price of trade tool.

        * __tablename__     - Table name in db
        * price             - Price
        * created_time      - Created time
        * trade_tool_id     - Identifier of trade tool
        * trade_tool        - Instance of model TradeTool
    """
    __tablename__ = "price_history"

    price = Column(Integer)
    created_time = Column(TIMESTAMP)
    trade_tool_id = Column(Integer, ForeignKey("trade_tool.id"), index=True)
    trade_tool = relationship("TradeTool", back_populates="history_prices")

    @classmethod
    def create_batch(cls, prices_info: List[tuple]) -> "Base":
        """
        Create multiply rows in table `price_history`

        Parameters
        ----------
        prices_info: List of tuple. [trade_tool_id, price, created_time), ...]

        Returns
        -------
        None
        """
        values = ', '.join([f"({_id}, {price}, '{date}'::timestamp)" for _id, price, date in prices_info])
        sql_raw = f"""
        INSERT INTO price_history (trade_tool_id, price, created_time)
        VALUES {values}
        """
        cls._manager.execute_sql(raw=sql_raw)

    @classmethod
    def get_history_prices(cls, trade_tool_id: int) -> List[dict]:
        """
        Get history prices of specific Trade tool.

        Parameters
        ----------
        trade_tool_id: Identifier of trade tool.

        Returns
        -------
        List of dict
        """
        with cls._manager.session() as session:
            result = session.query(cls.price, cls.created_time).filter(cls.trade_tool_id == trade_tool_id).all()
        return [{"x": int(update_date.timestamp()), "y": price} for price, update_date in result]


def create_default_data() -> None:
    """
    Create default data.

    100 records with the name `ticker_N` will be added to the `trade_tool` table, where `N` is the ordinal number.
    """
    for i in range(1, 101):
        try:
            TradeTool.create(name=f'ticker_{i}', last_price=0)
        except IntegrityError:
            continue


def migrate() -> None:
    """Apply migrations to database and create default data."""
    Base.metadata.create_all(bind=engine)
    create_default_data()
