from dataclasses import dataclass

@dataclass(frozen=True)
class ExceptionDTO:
        status_code: int
        message: str
