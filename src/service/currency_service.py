import logging

from fastapi import status
from sqlalchemy.exc import SQLAlchemyError, NoResultFound, IntegrityError

from src.dao.currencyDAO import CurrencyDAO
from src.dto.currencyDTO import CurrencyDTO
from src.dto.exceptionDTO import ExceptionDTO
from src.model.models import Currencies

logger = logging.getLogger("base")


class CurrencyService:
    @staticmethod
    def get_currency_dto(db_row: Currencies) -> CurrencyDTO | ExceptionDTO:
        try:
            currency = CurrencyDTO(
                id=db_row.id,
                code=db_row.code,
                name=db_row.name,
                sign=db_row.sign
            )
            return currency
        except TypeError as e:
            logger.error(e)
            return ExceptionDTO(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                message="Ошибка сервера")

    @classmethod
    async def get_currency(cls, code: str) -> CurrencyDTO | ExceptionDTO:
        try:
            db_response = await CurrencyDAO.get_currency(code)
        except NoResultFound as e:
            logger.info(e)
            exception_message = ExceptionDTO(status_code=status.HTTP_404_NOT_FOUND,
                                             message=f"Валюта с кодом {code} не найдена.")
            return exception_message
        except SQLAlchemyError as e:
            logger.error(e.args)
            exception_message = ExceptionDTO(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                             message="База данных недоступна.")
            return exception_message
        try:
            currency = cls.get_currency_dto(db_response)
            return currency
        except TypeError as e:
            logger.error(e)
            exception_message = ExceptionDTO(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                message="Ошибка сервера")
            return exception_message

    @classmethod
    async def get_currencies(cls) -> list[CurrencyDTO] | ExceptionDTO:
        try:
            db_response = await CurrencyDAO.get_currencies()
        except SQLAlchemyError as e:
            logger.error(e.args)
            exception_message = ExceptionDTO(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                             message="База данных недоступна.")
            return exception_message
        currencies = [cls.get_currency_dto(row) for row in db_response]
        return currencies

    @classmethod
    async def create_currency(cls, code: str,
                              name: str,
                              sign: str
                              ) -> CurrencyDTO | ExceptionDTO:
        try:
            db_response = await CurrencyDAO.create_currency(code=code, name=name, sign=sign)
        except IntegrityError as e:
            logger.error(e.args)
            exception_message = ExceptionDTO(status_code=status.HTTP_409_CONFLICT,
                                             message="Такая валюта уже добавлена.")
            return exception_message
        except SQLAlchemyError as e:
            logger.error(e)
            exception_message = ExceptionDTO(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                             message="База данных недоступна.")
            return exception_message
        currency = cls.get_currency_dto(db_response)
        return currency