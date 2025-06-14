from src.dao.currencyDAO import CurrencyDAO
from src.dto.currencyDTO import CurrencyDTO
from src.model.models import Currencies

from fastapi import status
from fastapi.exceptions import HTTPException

class CurrencyService:
    @staticmethod
    def get_currency_dto(db_row: Currencies) -> CurrencyDTO:
        try:
            currency = CurrencyDTO(
                id=db_row.id,
                code=db_row.code,
                name=db_row.name,
                sign=db_row.sign
            )
            return currency
        except TypeError as e:
            #todo logger
            print(e)
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @classmethod
    async def get_currency(cls, code: str) -> CurrencyDTO:
        db_response = await CurrencyDAO.get_currency(code)
        currency = cls.get_currency_dto(db_response)
        return currency

    @classmethod
    async def get_currencies(cls) -> list[CurrencyDTO]:
        db_response = await CurrencyDAO.get_currencies()
        currencies = [cls.get_currency_dto(row) for row in db_response]
        return currencies

    @classmethod
    async def create_currency(cls, code: str, name: str, sign: str):
        db_response = await CurrencyDAO.create_currency(code=code, name=name, sign=sign)
        currency = cls.get_currency_dto(db_response)
        return currency