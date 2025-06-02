from src.dto.currencyDTO import CurrencyDTO
from src.model.models import Currencies
from fastapi import status
from fastapi.exceptions import HTTPException

class CurrenciesDtoHandler:
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
