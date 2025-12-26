from sqlalchemy.orm import Session
from app.db.models import (PortfolioDB, OrderDB, TradeDB, PositionDB)

def get_or_create_portfolio(db: Session) -> PortfolioDB:
    portfolio = db.query(PortfolioDB).first()
    if portfolio is None:
        portfolio = PortfolioDB(balance_usd=10_000.0)
        db.add(portfolio)
        db.commit()
        db.refresh(portfolio)
    return portfolio

def get_position(db: Session, symbol: str) -> PositionDB | None:
    return db.query(PositionDB).filter_by(symbol=symbol).first()

def get_portfolio(db: Session) -> PortfolioDB:
    return db.query(PortfolioDB).first()

def get_positions(db: Session):
    return db.query(PositionDB).all()

def get_trades(db: Session, limit: int = 100):
    return (
        db.query(TradeDB).order_by(TradeDB.executed_at.desc()).limit(limit).all()
    )
