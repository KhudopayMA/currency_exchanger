from typing import Annotated

from fastapi import APIRouter, Query

from src.dto.currencyDTO import CurrencyDTO
from src.service.currency_service import CurrencyService

router = APIRouter(tags=["currencies"])

@router.get("/currencies")
async def get_currencies() -> list[CurrencyDTO]:
    return await CurrencyService.get_currencies()

@router.get("/currency/{code}")
async def get_currency(code: str) -> CurrencyDTO:
    return await CurrencyService.get_currency(code)

@router.post("/currencies", status_code=201)
async def create_currency(code: Annotated[str, Query(max_lengt=3)],
                          name: Annotated[str, Query(max_length=50)],
                          sign: Annotated[str, Query(max_length=5)]
                          ) -> CurrencyDTO:
    return await CurrencyService.create_currency(code=code, name=name, sign=sign)
