from sqlalchemy import select, insert

from src.model.models import Currencies
from src.database.database import DataBase

class CurrencyDAO:
    """Класс для выполнения запросов к БД для таблицы currencies"""

    model = Currencies

    @classmethod
    async def get_currencies(cls) -> list[Currencies]:
        async with DataBase.session() as session:
            statement = select(cls.model).order_by(cls.model.id)
            result = await session.execute(statement)
            rows = result.scalars().all()
            return rows


    @classmethod
    async def get_currency(cls, code: str) -> Currencies:
        async with DataBase.session() as session:
            statement = select(cls.model).where(cls.model.code == code)
            result = await session.execute(statement)
            currency = result.scalar_one()
            return currency

    @classmethod
    async def get_currency_id(cls, code: str) -> str:
        async with DataBase.session() as session:
            currency_id = await session.scalar(select(Currencies.id).
                                               where(Currencies.code == code))
            return currency_id


    @classmethod
    async def create_currency(cls, **kwargs) -> Currencies:
        async with DataBase.session() as session:
            statement = insert(cls.model).values(kwargs).returning(cls.model)
            result = await session.execute(statement)
            currency = result.scalar_one_or_none()
            await session.commit()
            await session.refresh(currency)
            return currency
