from decimal import Decimal

from sqlalchemy import select, insert, update, and_, DECIMAL
from sqlalchemy.orm import aliased
from sqlalchemy.exc import IntegrityError
from fastapi import status
from fastapi.exceptions import HTTPException

# from src.dao.baseDAO import BaseDAO
from src.dao.currencyDAO import CurrencyDAO
from src.database.database import DataBase
from src.model.models import ExchangeRates, Currencies

class ExchangeRateDAO:
    model = ExchangeRates

    @classmethod
    async def get_exchange_rate(cls, base_currency_code: str, target_currency_code: str):
        """Класс для выполнения запросов к БД для таблицы exchange_rates"""
        # todo alias для join
        base_currency = aliased(Currencies)
        target_currency = aliased(Currencies)
        async with DataBase.session() as session:
            statement = (select(cls.model)
                         .join(Currencies,
                              and_(base_currency.code == base_currency_code,
                                   base_currency.id == cls.model.base_currency_id)
                              )
                         .join(Currencies,
                               and_(target_currency.code == target_currency_code,
                                    target_currency.id == cls.model.target_currency_id)
                               )
                         )
            result = await session.execute(statement)
            exchange_rate = result.fetchone()
            return exchange_rate

    @classmethod
    async def create_exchange_rate(cls, base_currency_code: str, target_currency_code: str, rate: Decimal):
        async with DataBase.session() as session:
            base_currency_id = await session.scalar(select(Currencies.id).
                                                     where(Currencies.code == base_currency_code))
            if base_currency_id is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Валюта с кодом {base_currency_code} не существует в БД")
            target_currency_id = await session.scalar(select(Currencies.id).
                                                       where(Currencies.code == target_currency_code))
            if target_currency_id is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Валюта с кодом {target_currency_code} не существует в БД")
            new_exchange_rate = ExchangeRates(rate=rate,
                                             base_currency_id=base_currency_id,
                                             target_currency_id=target_currency_id)
            # await session.execute(insert(ExchangeRates).
            #                       values(base_currency_id=new_exchange_rate.base_currency_id,
            #                              target_currency_id=new_exchange_rate.target_currency_id,
            #                              rate=new_exchange_rate.rate
            #                              )
            #                       )

            session.add(new_exchange_rate)

            try:
                #todo scoped_session для решения raise condition
                await session.flush()
                # await session.refresh(new_exchange_rate)
                return new_exchange_rate
            except IntegrityError as e:
                print(e.args)
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail="Валютная пара с таким кодом уже существует")


    @classmethod
    async def update_exchange_rate(cls, base_currency_code: str, target_currency_code: str, rate: DECIMAL):
        async with (DataBase.session() as session):
            base_currency_id = await session.execute(select(Currencies.id).where(Currencies.code == base_currency_code))
            target_currency_id = await session.execute(select(Currencies.id).where(Currencies.code == target_currency_code))
            statement = (update(cls.model)
                        .where(and_(cls.model.base_currency_id == base_currency_id,
                                    cls.model.target_currency_id == target_currency_id)
                        )
                        .values(rate=rate)
                         )
            await session.execute(statement)
