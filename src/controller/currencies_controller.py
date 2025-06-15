from typing import Annotated

from fastapi import APIRouter, Query, Path
from fastapi.exceptions import HTTPException

from src.dto.currencyDTO import CurrencyDTO
from src.dto.exceptionDTO import ExceptionDTO
from src.service.currency_service import CurrencyService

router = APIRouter(tags=["currencies"])

@router.get("/currencies")
async def get_currencies() -> list[CurrencyDTO] | ExceptionDTO:
    response = await CurrencyService.get_currencies()
    if isinstance(response, ExceptionDTO):
        raise HTTPException(status_code=response.status_code, detail=response.message)
    return response

@router.get("/currency/{code}")
async def get_currency(code: Annotated[str, Path(min_length=3, max_length=3)]) -> CurrencyDTO | ExceptionDTO:
    response = await CurrencyService.get_currency(code)
    if isinstance(response, ExceptionDTO):
        raise HTTPException(status_code=response.status_code, detail=response.message)
    return response

@router.post("/currencies", status_code=201)
async def create_currency(code: Annotated[str, Query(max_lengt=3)],
                          name: Annotated[str, Query(max_length=50)],
                          sign: Annotated[str, Query(max_length=5)]
                          ) -> CurrencyDTO | ExceptionDTO:
    response = await CurrencyService.create_currency(code=code, name=name, sign=sign)
    if isinstance(response, ExceptionDTO):
        raise HTTPException(status_code=response.status_code, detail=response.message)
    return response
