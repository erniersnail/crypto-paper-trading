# app/trading/models.py

from dataclasses import dataclass


@dataclass
class Order:
    symbol: str
    side: str
    qty: float
    price: float


@dataclass
class Trade:
    symbol: str
    side: str
    qty: float
    price: float
