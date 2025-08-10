from decimal import Decimal

from sqlalchemy import select, update, and_
from sqlalchemy.orm import selectinload

from src.database.database import DataBase
from src.model.models import ExchangeRates, Currencies


class ExchangeRateDAO:
    model = ExchangeRates

    @classmethod
    async def get_exchange_rates(cls) -> list[ExchangeRates]:
        async with (DataBase.session() as session):
            statement = (select(cls.model)
                        .options(selectinload(cls.model.base_currency),
                                 selectinload(cls.model.target_currency))
                        )
            result = await session.execute(statement)
            exchange_rates = result.scalars().all()
            return exchange_rates

    @classmethod
    async def get_exchange_rate(cls, base_currency: Currencies, target_currency: Currencies
                                ) -> ExchangeRates:
        async with DataBase.session() as session:
            exchange_rate = await session.execute(
                select(cls.model).
                where(and_
                    (
                        cls.model.base_currency_id == base_currency.id,
                        cls.model.target_currency_id == target_currency.id
                    )
                ).
                options(selectinload(cls.model.base_currency), selectinload(cls.model.target_currency))
            )
            return exchange_rate.scalar_one_or_none()

    @classmethod
    async def create_exchange_rate(cls, base_currency_id: str, target_currency_id: str, rate: Decimal
                                   ) -> ExchangeRates:
        async with DataBase.session() as session:
            new_exchange_rate = ExchangeRates(rate=rate,
                                             base_currency_id=base_currency_id,
                                             target_currency_id=target_currency_id)
            session.add(new_exchange_rate)
            await session.commit()
            exchange_rate = await session.execute(
                select(cls.model).
                where(cls.model.id == new_exchange_rate.id).
                options(selectinload(cls.model.base_currency), selectinload(cls.model.target_currency))
            )
            return exchange_rate.scalars().first()

    @classmethod
    async def update_exchange_rate(cls, base_currency: Currencies, target_currency: Currencies, rate: Decimal
                                   ) -> ExchangeRates:
        async with (DataBase.session() as session):
            statement = (update(cls.model).
                        where(and_(
                                    cls.model.base_currency_id == base_currency.id,
                                    cls.model.target_currency_id == target_currency.id)).
                        values(rate=rate).
                        returning(cls.model).
                        options(selectinload(cls.model.base_currency), selectinload(cls.model.target_currency))
                         )
            db_result = await session.execute(statement)
            exchange_rate = db_result.scalar_one()
            await session.commit()
            return exchange_rate
