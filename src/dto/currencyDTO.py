from dataclasses import dataclass

@dataclass(frozen=True)
class CurrencyDTO:
    id: int
    code: str
    name: str
    sign: str
