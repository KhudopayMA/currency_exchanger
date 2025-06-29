from decimal import Decimal

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError, NoResultFound, MultipleResultsFound

from src.dto.exchange_ratesDTO import ExchangeRatesDTO, ExchangeRatesWithCurrenciesDTO, ExchangeDTO
from src.dto.exceptionDTO import ExceptionDTO
from src.dao.exchange_rateDAO import ExchangeRateDAO
from src.dao.currencyDAO import CurrencyDAO
from src.model.models import ExchangeRates, Currencies
from src.service.currency_service import CurrencyService


class ExchangeRateService:
    @staticmethod
    def get_exchange_rate_dto(db_row: ExchangeRates) -> ExchangeRatesDTO | ExceptionDTO:
        try:
            exchange_rate = ExchangeRatesDTO(
                id=db_row.id,
                base_currency_id=db_row.base_currency_id,
                target_currency_id=db_row.target_currency_id,
                rate=db_row.rate)
            return exchange_rate
        except TypeError as e:
            print(e)
            # raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
            return ExceptionDTO(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                message="Ошибка сервера")

    @staticmethod
    def get_exchange_rates_with_currencies_dto(db_row: ExchangeRates
                                               ) -> ExchangeRatesWithCurrenciesDTO | ExceptionDTO:
        try:
            exchange_rate = ExchangeRatesWithCurrenciesDTO(
                id=db_row.id,
                base_currency=CurrencyService.get_currency_dto(db_row.base_currency),
                target_currency=CurrencyService.get_currency_dto(db_row.target_currency),
                rate=db_row.rate.normalize()
            )
            return exchange_rate
        except TypeError as e:
            #todo logger
            print(e)
            # raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
            return ExceptionDTO(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                message="Ошибка сервера")

    @staticmethod
    def get_exchange_dto(db_row: ExchangeRates,
                         amount: Decimal,
                         converted_amount: Decimal
                         ) -> ExchangeDTO | ExceptionDTO:
        try:
            exchange = ExchangeDTO(
                id=db_row.id,
                base_currency=CurrencyService.get_currency_dto(db_row.base_currency),
                target_currency=CurrencyService.get_currency_dto(db_row.target_currency),
                rate=db_row.rate.normalize(),
                amount=amount,
                converted_amount=converted_amount
            )
            return exchange
        except TypeError as e:
            # todo logger
            print(e)
            # raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)\
            return ExceptionDTO(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                message="Ошибка сервера")

    @classmethod
    async def get_exchange_rates(cls) -> list[ExchangeRatesWithCurrenciesDTO] | ExceptionDTO:
        try:
            db_response = await ExchangeRateDAO.get_exchange_rates()
        except SQLAlchemyError as e:
            print(e)
            exception_message = ExceptionDTO(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                 message="База данных недоступна.")
            return exception_message
        exchange_rates = [ExchangeRateService.get_exchange_rates_with_currencies_dto(row) for row in db_response]
        return exchange_rates

    @classmethod
    async def get_exchange_rate(cls, currencies_pair: str) -> ExchangeRatesWithCurrenciesDTO | ExceptionDTO:
        try:
            try:
                base_currency = await CurrencyDAO.get_currency(currencies_pair[:3])
            except NoResultFound as e:
                print(e.args)
                exception_message = ExceptionDTO(status_code=status.HTTP_404_NOT_FOUND,
                                                 message=f"Валюта с кодом {currencies_pair[:3]} не найдена.")
                return exception_message
            try:
                target_currency = await CurrencyDAO.get_currency(currencies_pair[3:])
            except NoResultFound as e:
                print(e.args)
                exception_message = ExceptionDTO(status_code=status.HTTP_404_NOT_FOUND,
                                                 message=f"Валюта с кодом {currencies_pair[3:]} не найдена.")
                return exception_message
            db_response = await ExchangeRateDAO.get_exchange_rate(base_currency, target_currency)
            if db_response is None:
                #todo logg
                exception_message = ExceptionDTO(status_code=status.HTTP_404_NOT_FOUND,
                                                 message="Обменный курс для пары не найден")
                return exception_message
            exchange_rate = ExchangeRateService.get_exchange_rates_with_currencies_dto(db_response)
            return exchange_rate
        except SQLAlchemyError as e:
            # todo logger
            print(e.args)
            exception_message = ExceptionDTO(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                             message="База данных недоступна.")
            return exception_message

    @classmethod
    async def create_exchange_rates(cls,
                                    base_currency_code: str,
                                    target_currency_code: str,
                                    rate: Decimal
                                    ) -> ExchangeRatesWithCurrenciesDTO | ExceptionDTO:
        try:
            try:
                base_currency_id = await CurrencyDAO.get_currency_id(base_currency_code)
            except NoResultFound as e:
                print(e.args)
                exception_message = ExceptionDTO(status_code=status.HTTP_404_NOT_FOUND,
                                                 message=f"Валюта с кодом {base_currency_code} не найдена.")
                return exception_message
            try:
                target_currency_id = await CurrencyDAO.get_currency_id(target_currency_code)
            except NoResultFound as e:
                print(e.args)
                exception_message = ExceptionDTO(status_code=status.HTTP_404_NOT_FOUND,
                                                 message=f"Валюта с кодом {target_currency_code} не найдена.")
                return exception_message
            db_response = await ExchangeRateDAO.create_exchange_rate(base_currency_id=base_currency_id,
                                                                     target_currency_id=target_currency_id,
                                                                     rate=rate)
            created_exchange_rate = ExchangeRateService.get_exchange_rates_with_currencies_dto(db_response)
            return created_exchange_rate
        except SQLAlchemyError as e:
            # todo logger
            print(e.args)
            exception_message = ExceptionDTO(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                             message="База данных недоступна.")
            return exception_message


    @classmethod
    async def update_exchange_rates(cls,
                                    currencies_pair: str,
                                    rate: Decimal
                                    ) -> ExchangeRatesWithCurrenciesDTO | ExceptionDTO:
        try:
            try:
                base_currency = await CurrencyDAO.get_currency(currencies_pair[0:3])
            except NoResultFound as e:
                print(e.args)
                exception_message = ExceptionDTO(status_code=status.HTTP_404_NOT_FOUND,
                                                 message=f"Валюта с кодом {currencies_pair[:3]} не найдена.")
                return exception_message
            try:
                target_currency = await CurrencyDAO.get_currency(currencies_pair[3:])
            except NoResultFound as e:
                print(e.args)
                exception_message = ExceptionDTO(status_code=status.HTTP_404_NOT_FOUND,
                                                 message=f"Валюта с кодом {currencies_pair[3:]} не найдена.")
                return exception_message
            try:
                db_response = await ExchangeRateDAO.update_exchange_rate(base_currency=base_currency,
                                                                       target_currency=target_currency,
                                                                       rate=rate)
                updated_exchange_rate = ExchangeRateService.get_exchange_rates_with_currencies_dto(db_response)
                return updated_exchange_rate
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
        except SQLAlchemyError as e:
            # todo logger
            print(e.args)
            exception_message = ExceptionDTO(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                             message="База данных недоступна.")
            return exception_message

    @classmethod
    async def get_exchange(cls,
                           currency_from: str,
                           currency_to: str,
                           amount: Decimal
                           ) -> ExchangeDTO | ExceptionDTO:
        try:
            try:
                base_currency = await CurrencyDAO.get_currency(currency_from)
            except NoResultFound as e:
                print(e.args)
                exception_message = ExceptionDTO(status_code=status.HTTP_404_NOT_FOUND,
                                                 message=f"Валюта с кодом {currency_from} не найдена.")
                return exception_message
            try:
                target_currency = await CurrencyDAO.get_currency(currency_to)
            except NoResultFound as e:
                print(e.args)
                exception_message = ExceptionDTO(status_code=status.HTTP_404_NOT_FOUND,
                                                 message=f"Валюта с кодом {currency_to} не найдена.")
                return exception_message

            direct_course = await ExchangeRateDAO.get_exchange_rate(base_currency=base_currency,
                                                                target_currency=target_currency)
            if isinstance(direct_course, ExchangeRates):
                converted_amount = (direct_course.rate.normalize() * amount.normalize()).quantize(Decimal("1.00"))
                exchange = cls.get_exchange_dto(db_row=direct_course,
                                                amount=amount,
                                                converted_amount=converted_amount)
                return exchange

            reverse_course = await ExchangeRateDAO.get_exchange_rate(base_currency=target_currency,
                                                                target_currency=base_currency)
            if isinstance(reverse_course, ExchangeRates):
                converted_amount = (amount.normalize() / reverse_course.rate.normalize()).quantize(Decimal("1.00"))
                exchange = cls.get_exchange_dto(db_row=reverse_course,
                                                amount=amount,
                                                converted_amount=converted_amount)
                return exchange

            exception_message = ExceptionDTO(status_code=status.HTTP_404_NOT_FOUND,
                                             message="Обменный курс для пары не найден")
            return exception_message
        except SQLAlchemyError as e:
            # todo logger
            print(e.args)
            exception_message = ExceptionDTO(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                             message="База данных недоступна.")
            return exception_message
