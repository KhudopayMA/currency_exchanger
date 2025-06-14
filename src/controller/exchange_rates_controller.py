from typing import Annotated
from decimal import Decimal

from fastapi import APIRouter, Form, Path, Query

from src.dao.exchange_rateDAO import ExchangeRateDAO
from src.dao.currencyDAO import CurrencyDAO
from src.service.exchange_rate_service import ExchangeRateService
from src.dto.exchange_ratesDTO import ExchangeRatesWithCurrenciesDTO

router = APIRouter(tags=["exchange_rates"])

@router.get("/exchangeRates")
async def get_exchange_rates() -> list[ExchangeRatesWithCurrenciesDTO]:
    return await ExchangeRateService.get_exchange_rates()

@router.get("/exchangeRate/{currencies_pair}")
async def get_exchange_rate(currencies_pair: Annotated[str, Path(min_length=6, max_length=6)]
                            ) -> ExchangeRatesWithCurrenciesDTO:
    return await ExchangeRateService.get_exchange_rate(currencies_pair)


@router.post("/exchangeRates")
async def create_exchange_rates(base_currency_code: Annotated[str, Form()],
                                target_currency_code: Annotated[str, Form()],
                                rate: Annotated[Decimal, Form()]
                                ) -> ExchangeRatesWithCurrenciesDTO:
    return await ExchangeRateService.create_exchange_rates(base_currency_code=base_currency_code,
                                                           target_currency_code=target_currency_code,
                                                           rate=rate)


@router.patch("/exchangeRate/{currencies_pair}")
async def update_exchange_rates(currencies_pair: str,
                                rate: Annotated[Decimal, Form()]):
    return await ExchangeRateService.update_exchange_rates(currencies_pair=currencies_pair,
                                                           rate=rate)

@router.get("/exchange")
async def get_exchange(
        currency_from: Annotated[str, Query(alias="from")],
        currency_to: Annotated[str, Query(alias="to")],
        amount: Decimal
):
    base_currency = await CurrencyDAO.get_currency(currency_from)
    target_currency = await CurrencyDAO.get_currency(currency_to)
    # todo передать валюты в service
    db_result = await ExchangeRateDAO.get_exchange_rate(base_currency, target_currency)

