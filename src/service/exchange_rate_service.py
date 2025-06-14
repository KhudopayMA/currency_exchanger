from decimal import Decimal

from src.dto.exchange_ratesDTO import ExchangeRatesDTO, ExchangeRatesWithCurrenciesDTO
from src.dao.exchange_rateDAO import ExchangeRateDAO
from src.dao.currencyDAO import CurrencyDAO
from src.model.models import ExchangeRates
from src.service.currency_service import CurrencyService

from fastapi import status
from fastapi.exceptions import HTTPException

class ExchangeRateService:
    @staticmethod
    def get_exchange_rate_dto(db_row: ExchangeRates) -> ExchangeRatesDTO:
        try:
            exchange_rate = ExchangeRatesDTO(
                id=db_row.id,
                base_currency_id=db_row.base_currency_id,
                target_currency_id=db_row.target_currency_id,
                rate=db_row.rate)

            return exchange_rate
        except TypeError as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @staticmethod
    def get_exchange_rates_with_currencies_dto(db_row: ExchangeRates) -> ExchangeRatesWithCurrenciesDTO:
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
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @classmethod
    async def get_exchange_rates(cls) -> list[ExchangeRatesWithCurrenciesDTO]:
        db_result = await ExchangeRateDAO.get_exchange_rates()
        exchange_rates = [ExchangeRateService.get_exchange_rates_with_currencies_dto(row) for row in db_result]
        return exchange_rates

    @classmethod
    async def get_exchange_rate(cls, currencies_pair: str) -> ExchangeRatesWithCurrenciesDTO:
        base_currency = await CurrencyDAO.get_currency(currencies_pair[:3])
        target_currency = await CurrencyDAO.get_currency(currencies_pair[3:])
        db_result = await ExchangeRateDAO.get_exchange_rate(base_currency, target_currency)
        exchange_rate = ExchangeRateService.get_exchange_rates_with_currencies_dto(db_result)
        return exchange_rate

    @classmethod
    async def create_exchange_rates(cls,
                                    base_currency_code: str,
                                    target_currency_code: str,
                                    rate: Decimal
                                    ) -> ExchangeRatesWithCurrenciesDTO:
        db_result = await ExchangeRateDAO.create_exchange_rate(base_currency_code=base_currency_code,
                                                               target_currency_code=target_currency_code,
                                                               rate=rate)
        created_exchange_rate = ExchangeRateService.get_exchange_rates_with_currencies_dto(db_result)
        return created_exchange_rate

    @classmethod
    async def update_exchange_rates(cls,
                                    currencies_pair: str,
                                    rate: Decimal
                                    ) -> ExchangeRatesWithCurrenciesDTO:
        base_currency = await CurrencyDAO.get_currency(currencies_pair[0:3])
        target_currency = await CurrencyDAO.get_currency(currencies_pair[3:])
        db_result = await ExchangeRateDAO.update_exchange_rate(base_currency=base_currency,
                                                               target_currency=target_currency,
                                                               rate=rate)
        updated_exchange_rate = ExchangeRateService.get_exchange_rates_with_currencies_dto(db_result)
        return updated_exchange_rate

