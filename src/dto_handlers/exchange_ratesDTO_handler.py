from src.dto.exchange_ratesDTO import ExchangeRatesDTO
from src.model.models import ExchangeRates
from fastapi import status
from fastapi.exceptions import HTTPException

class ExchangeRatesDtoHandler:
    @staticmethod
    def get_exchange_rates_dto(db_row: ExchangeRates) -> ExchangeRatesDTO:
        try:
            exchange_rate = ExchangeRatesDTO(
                id=db_row.id,
                base_currency=db_row.base_currency,
                target_currency=db_row.target_currency,
                rate=db_row.rate
            )
            return exchange_rate
        except TypeError as e:
            #todo logger
            print(e)
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
