from decimal import Decimal

from sqlalchemy import String, DECIMAL, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.model.base import Base

class Currencies(Base):
    """
    Класс для хранения данных о валюте
    """
    __tablename__ = "currencies"

    code: Mapped[str] = mapped_column(String(3), unique=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    sign: Mapped[str] = mapped_column(String(3), unique=True)

    # base_exchange_rates: Mapped["ExchangeRates"] = relationship(back_populates="base_currency")
    # target_exchange_rates: Mapped["ExchangeRates"] = relationship(back_populates="target_currency")

class ExchangeRates(Base):
    """
    Класс для хранения данных об обменном курсе валют
    """

    __tablename__ = "exchange_rates"

    base_currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id", ondelete="CASCADE"))
    target_currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id", ondelete="CASCADE"))
    rate: Mapped[Decimal] = mapped_column(DECIMAL(precision=10, scale=6), nullable=False)

    base_currency: Mapped["Currencies"] = relationship(foreign_keys="[ExchangeRates.base_currency_id]")
    target_currency: Mapped["Currencies"] = relationship(foreign_keys="[ExchangeRates.target_currency_id]")