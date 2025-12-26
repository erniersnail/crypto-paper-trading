from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.db.base import Base

class PortfolioDB(Base):
    __tablename__ = "portfolios"
    id = Column(Integer, primary_key=True)
    balance_usd = Column(Float, nullable=False, default=10_000.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class OrderDB(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    symbol = Column(String, index=True)
    side = Column(String)  # BUY / SELL
    qty = Column(Float)
    price = Column(Float)
    status = Column(String)  # OPEN / FILLED / CANCELLED
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TradeDB(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    symbol = Column(String)
    side = Column(String)
    qty = Column(Float)
    price = Column(Float)
    executed_at = Column(DateTime(timezone=True), server_default=func.now())


class PositionDB(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True)
    symbol = Column(String, unique=True)
    qty = Column(Float)
    avg_price = Column(Float)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
