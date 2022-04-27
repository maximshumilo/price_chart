from typing import Optional, Type, List

from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import config


engine = create_engine(config.DATABASE_URL)
Base = declarative_base()


class DatabaseManager:
    """A manager for interacting with the database."""

    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    @classmethod
    def get_by_id(cls, target_model: Type["BaseModelMixin"], target_id: int) -> Optional[Base]:
        """
        Get instance of target model by id.

        Parameters
        ----------
        target_model: Target model type
        target_id: Target id

        Returns
        -------
        Instance of target model or None
        """
        with cls.session() as session:
            return session.query(target_model).filter(target_model.id == target_id).first()

    @classmethod
    def all(cls, target_model: Type["BaseModelMixin"]) -> List[Base]:
        """
        Get all rows from db by model.

        Parameters
        ----------
        target_model: Model

        Returns
        -------
        List of instances.
        """
        with cls.session() as session:
            return session.query(target_model).all()

    @classmethod
    def create(cls, instance: Base) -> Base:
        """
        Adds a row to the model table, and returns its instance.

        Parameters
        ----------
        instance: Instance of model

        Returns
        -------
        Instance of `target_model`
        """
        with cls.session() as session:
            session.merge(instance)
            session.commit()
        return instance

    @staticmethod
    def execute_sql(raw: str) -> None:
        """
        Execute SQL query.

        Parameters
        ----------
        raw: SQL raw

        Returns
        -------
        None
        """
        with engine.connect() as con:
            con.execute(raw)


class BaseModelMixin(object):
    """
    Mixin base model.

    Includes the `id` field.
    And also an open method of the class: create. It accesses the `DatabaseManager`
    """

    _manager = DatabaseManager

    id = Column(Integer, primary_key=True, index=True)

    @classmethod
    def get_by_id(cls, target_id: int) -> Optional[Base]:
        """
        Get instance by id.

        Parameters
        ----------
        target_id: Identifier

        Returns
        -------
        Instance or None
        """
        return cls._manager.get_by_id(target_model=cls, target_id=target_id)

    @classmethod
    def all(cls) -> List[Base]:
        """
        Get all instances.

        Returns
        -------
        List of Instances.
        """
        return cls._manager.all(target_model=cls)

    @classmethod
    def create(cls, **kwargs) -> Base:
        """
        Insert raw to database by this model.

        Parameters
        ----------
        kwargs: Data of model

        Returns
        -------
        Instance
        """
        return cls._manager.create(instance=cls(**kwargs))
