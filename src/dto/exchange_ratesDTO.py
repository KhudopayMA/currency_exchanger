from dataclasses import dataclass

from src.dto.currencyDTO import CurrencyDTO

@dataclass(frozen=True)
class ExchangeRatesDTO:
    id: int
    base_currency: CurrencyDTO
    target_currency: CurrencyDTO
    rate: float
