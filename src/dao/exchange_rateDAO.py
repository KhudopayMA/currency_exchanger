from decimal import Decimal

from sqlalchemy import select, update, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError, NoResultFound, MultipleResultsFound, SQLAlchemyError
from fastapi import status

from src.database.database import DataBase
from src.model.models import ExchangeRates, Currencies
from src.dto.exceptionDTO import ExceptionDTO
class ExchangeRateDAO:
    model = ExchangeRates

    @classmethod
    async def get_exchange_rates(cls) -> list[ExchangeRates] | ExceptionDTO:
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
                                ) -> ExchangeRates | ExceptionDTO:
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
             exception_message = ExceptionDTO(status_code=status.HTTP_404_NOT_FOUND,
                                                  message="Обменный курс для пары не найден")
             return exception_message
        except SQLAlchemyError as e:
            print(e)
            exception_message = ExceptionDTO(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                 message="База данных недоступна.")
            return exception_message

    @classmethod
    async def create_exchange_rate(cls, base_currency_code: str, target_currency_code: str, rate: Decimal
                                   ) -> ExchangeRates | ExceptionDTO:
        async with DataBase.session() as session:
            base_currency_id = await session.scalar(select(Currencies.id).
                                                     where(Currencies.code == base_currency_code))
            if base_currency_id is None:
                exception_message = ExceptionDTO(status_code=status.HTTP_404_NOT_FOUND,
                                                     message=f"Валюта с кодом {base_currency_code} не существует в БД")
                return exception_message
            target_currency_id = await session.scalar(select(Currencies.id).
                                                       where(Currencies.code == target_currency_code))
            if target_currency_id is None:
                exception_message = ExceptionDTO(status_code=status.HTTP_404_NOT_FOUND,
                                                     message=f"Валюта с кодом {target_currency_code} не существует в БД")
                return exception_message
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
                exception_message = ExceptionDTO(status_code=status.HTTP_409_CONFLICT,
                                                     message=f"Валюта с кодом {target_currency_code} не существует в БД")
                return exception_message

    @classmethod
    async def update_exchange_rate(cls, base_currency: Currencies, target_currency: Currencies, rate: Decimal
                                   ) -> ExchangeRates | ExceptionDTO:
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
            exception_message = ExceptionDTO(status_code=status.HTTP_404_NOT_FOUND,
                                             message="Валютная пара отсутствует в базе данных")
            return exception_message
        except MultipleResultsFound as e:
            # todo сделать constraint в бд что пара валют не может повторяться
            print(e)
            exception_message = ExceptionDTO(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                             message="Было найдено несколько записей валютной пары.")
            return exception_message
        except SQLAlchemyError as e:
            print(e)
            exception_message = ExceptionDTO(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                             message="База данных недоступна.")
            return exception_message


