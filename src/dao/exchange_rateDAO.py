from decimal import Decimal

from sqlalchemy import select, update, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError, NoResultFound, MultipleResultsFound, SQLAlchemyError
from fastapi import status
from fastapi.exceptions import HTTPException

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
    async def get_exchange_rate(cls, base_currency: Currencies, target_currency: Currencies):
        try:
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
                return exchange_rate.scalar_one()
        except NoResultFound as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Обменный курс для пары не найден")
        except SQLAlchemyError as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="База данных недоступна.")

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
            try:
                #todo scoped_session для решения raise condition
                session.add(new_exchange_rate)
                await session.commit()
                exchange_rate = await session.execute(
                    select(cls.model).
                    where(cls.model.id == new_exchange_rate.id).
                    options(selectinload(cls.model.base_currency), selectinload(cls.model.target_currency))
                )
                return exchange_rate.scalars().first()
            except IntegrityError as e:
                print(e.args)
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail="Валютная пара с таким кодом уже существует")


    @classmethod
    async def update_exchange_rate(cls, base_currency: Currencies, target_currency: Currencies, rate: Decimal):
        try:
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
        except NoResultFound as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Валютная пара отсутствует в базе данных")
        except MultipleResultsFound as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Было найдено несколько записей валютной пары.")
        except SQLAlchemyError as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="База данных недоступна.")

