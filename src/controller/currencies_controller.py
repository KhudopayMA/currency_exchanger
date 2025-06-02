from typing import Annotated

from fastapi import APIRouter, Query

from src.dao.currencyDAO import CurrencyDAO
from src.dto_handlers.currenciesDTO_handler import CurrenciesDtoHandler

router = APIRouter(tags=["currencies"])

@router.get("/currencies")
async def get_currencies():
    db_response_list = await CurrencyDAO.get_currencies()
    currencies = [CurrenciesDtoHandler.get_currency_dto(currency) for currency in db_response_list]
    return currencies

@router.get("/currency/{code}")
async def get_currencies(code: str):
    db_response = await CurrencyDAO.get_currency(code)
    currency = CurrenciesDtoHandler.get_currency_dto(db_response)
    return currency

@router.post("/currencies", status_code=201)
async def create_currency(code: Annotated[str, Query(max_lengt=3)],
                          name: Annotated[str, Query(max_length=50)],
                          sign: Annotated[str, Query(max_length=5)]):
    db_response = await CurrencyDAO.create_currency(code=code, name=name, sign=sign)
    currency = CurrenciesDtoHandler.get_currency_dto(db_response)
    return currency
