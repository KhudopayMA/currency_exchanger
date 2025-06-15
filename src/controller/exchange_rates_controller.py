from typing import Annotated
from decimal import Decimal

from fastapi import APIRouter, Form, Path, Query
from fastapi.exceptions import HTTPException

from src.dao.exchange_rateDAO import ExchangeRateDAO
from src.dao.currencyDAO import CurrencyDAO
from src.service.exchange_rate_service import ExchangeRateService
from src.dto.exchange_ratesDTO import ExchangeRatesWithCurrenciesDTO, ExchangeDTO
from src.dto.exceptionDTO import ExceptionDTO

router = APIRouter(tags=["exchange_rates"])

@router.get("/exchangeRates")
async def get_exchange_rates() -> list[ExchangeRatesWithCurrenciesDTO] | ExceptionDTO:
    response = await ExchangeRateService.get_exchange_rates()
    return response

@router.get("/exchangeRate/{currencies_pair}")
async def get_exchange_rate(currencies_pair: Annotated[str, Path(min_length=6, max_length=6)]
                            ) -> ExchangeRatesWithCurrenciesDTO | ExceptionDTO:
    response =  await ExchangeRateService.get_exchange_rate(currencies_pair)
    return response

@router.post("/exchangeRates")
async def create_exchange_rates(base_currency_code: Annotated[str, Form()],
                                target_currency_code: Annotated[str, Form()],
                                rate: Annotated[Decimal, Form()]
                                ) -> ExchangeRatesWithCurrenciesDTO | ExceptionDTO:
    response =  await ExchangeRateService.create_exchange_rates(base_currency_code=base_currency_code,
                                                           target_currency_code=target_currency_code,
                                                           rate=rate)
    return response

@router.patch("/exchangeRate/{currencies_pair}")
async def update_exchange_rates(currencies_pair: str,
                                rate: Annotated[Decimal, Form()]
                                ) -> ExchangeRatesWithCurrenciesDTO | ExceptionDTO:
    response =  await ExchangeRateService.update_exchange_rates(currencies_pair=currencies_pair,
                                                           rate=rate)
    return response

@router.get("/exchange")
async def get_exchange(currency_from: Annotated[str, Query(alias="from")],
                       currency_to: Annotated[str, Query(alias="to")],
                       amount: Decimal
                      ) -> ExchangeDTO | ExceptionDTO:
    response = await ExchangeRateService.get_exchange(currency_from=currency_from,
                                                currency_to=currency_to,
                                                amount=amount)
    if isinstance(response, ExceptionDTO):
        raise HTTPException(status_code=response.status_code, detail=response.message)
    return response

