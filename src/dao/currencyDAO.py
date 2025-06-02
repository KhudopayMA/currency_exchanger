from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

# from src.dao.baseDAO import BaseDAO
from src.model.models import Currencies
from src.database.database import DataBase

class CurrencyDAO:
    """Класс для выполнения запросов к БД для таблицы currencies"""

    model = Currencies

    @classmethod
    async def get_currencies(cls):
        try:
            async with DataBase.session() as session:
                statement = select(cls.model).order_by(cls.model.id)
                result = await session.execute(statement)
                rows = result.scalars().all()
                return rows
        except SQLAlchemyError as e:
            # todo logger
            print(e.args)
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    @classmethod
    async def get_currency(cls, code: str):
        try:
            async with DataBase.session() as session:
                statement = select(cls.model).where(cls.model.code == code)
                result = await session.execute(statement)
                currency = result.scalar_one_or_none()
                if currency:
                    return currency
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Валюта с кодом {code} не найдена.")
        except SQLAlchemyError as e:
            # todo logger
            print(e.args)
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    @classmethod
    async def create_currency(cls, **kwargs):
        try:
            async with DataBase.session() as session:
                statement = insert(cls.model).values(kwargs).returning(cls.model)
                result = await session.execute(statement)
                currency = result.scalar_one_or_none()
                await session.commit()
                await session.refresh(currency)
                return currency
        except IntegrityError as e:
            print(e.args)
            # todo logger
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail= "Такая валюта уже добавлена.")
        except SQLAlchemyError as e:
            print(e.args)
            # todo logger
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)