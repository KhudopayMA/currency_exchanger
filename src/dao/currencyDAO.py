from fastapi import status
from sqlalchemy import select, insert
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, NoResultFound

from src.model.models import Currencies
from src.database.database import DataBase
from src.dto.exceptionDTO import ExceptionDTO

class CurrencyDAO:
    """Класс для выполнения запросов к БД для таблицы currencies"""

    model = Currencies

    @classmethod
    async def get_currencies(cls) -> list[Currencies] | ExceptionDTO:
        try:
            async with DataBase.session() as session:
                statement = select(cls.model).order_by(cls.model.id)
                result = await session.execute(statement)
                rows = result.scalars().all()
                return rows
        except SQLAlchemyError as e:
            # todo logger
            print(e.args)
            exception_message = ExceptionDTO(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                             message="База данных недоступна.")
            return exception_message

    @classmethod
    async def get_currency(cls, code: str) -> Currencies | ExceptionDTO:
        try:
            async with DataBase.session() as session:
                statement = select(cls.model).where(cls.model.code == code)
                result = await session.execute(statement)
                currency = result.scalar_one()
                return currency
        except NoResultFound as e:
            print(e.args)
            exception_message = ExceptionDTO(status_code=status.HTTP_404_NOT_FOUND,
                                             message=f"Валюта с кодом {code} не найдена.")
            return exception_message
        except SQLAlchemyError as e:
            # todo logger
            print(e.args)
            exception_message = ExceptionDTO(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                             message="База данных недоступна.")
            return exception_message

    @classmethod
    async def create_currency(cls, **kwargs) -> Currencies | ExceptionDTO:
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
            exception_message = ExceptionDTO(status_code=status.HTTP_409_CONFLICT,
                                             message="Такая валюта уже добавлена.")
            return exception_message
        except SQLAlchemyError as e:
            print(e.args)
            # todo logger
            exception_message = ExceptionDTO(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                             message="База данных недоступна.")
            return exception_message