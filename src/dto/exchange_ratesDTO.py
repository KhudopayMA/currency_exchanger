from dataclasses import dataclass
from decimal import Decimal

from src.dto.currencyDTO import CurrencyDTO

@dataclass(frozen=True)
class ExchangeRatesDTO:
    id: int
    base_currency_id: int
    target_currency_id: int
    rate: Decimal

@dataclass(frozen=True)
class ExchangeRatesWithCurrenciesDTO:
    id: int
    base_currency: CurrencyDTO
    target_currency: CurrencyDTO
    rate: Decimal

@dataclass(frozen=True)
class ExchangeDTO:
    id: int
    base_currency: CurrencyDTO
    target_currency: CurrencyDTO
    rate: Decimal
    amount: Decimal
    converted_amount: Decimal
