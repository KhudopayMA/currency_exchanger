from typing import Annotated
from decimal import Decimal

from fastapi import APIRouter, Form

from src.dao.exchange_rateDAO import ExchangeRateDAO
from src.dto_handlers.exchange_ratesDTO_handler import ExchangeRatesDTO

router = APIRouter(tags=["exchange_rates"])

@router.get("/exchangeRates")
async def get_exchange_rates():
    pass

@router.post("/exchangeRates")
async def create_exchange_rates(base_currency_code: Annotated[str, Form()],
                                target_currency_code: Annotated[str, Form()],
                                rate: Annotated[Decimal, Form()]):
    db_result = await ExchangeRateDAO.create_exchange_rate(base_currency_code=base_currency_code,
                                                     target_currency_code=target_currency_code,
                                                     rate=rate)
