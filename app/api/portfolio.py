from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.repository import (get_portfolio, get_positions, get_trades)

from app.market.state import get_price

router = APIRouter(prefix="/portfolio", tags=["portfolio"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("")
def portfolio(db: Session = Depends(get_db)):
    p = get_portfolio(db)
    return{
        "balance_usd": p.balance_usd if p else 0.00
    }

@router.get("/positions")
def positions(db: Session = Depends(get_db)):
    results = []
    for pos in get_positions(db):
        current_price = get_price(pos.symbol)
        unrealized = (
            (current_price - pos.avg_price) * pos.qty
            if current_price is not None else 0.0
        )
    results.append({
        "symbol": pos.symbol,
        "qty": pos.qty,
        "avg_price": pos.avg_price,
        "current_price": current_price,
        "unrealized_pnl": unrealized
    })

    return results

@router.get("/trades")
def trades(limit: int = 50, db: Session = Depends(get_db)):
    result = []

    for t in get_trades(db, limit):
        result.append({
            "symbol": t.symbol,
            "side": t.side,
            "qty": t.qty,
            "price": t.price,
            "executed_at": t.executed_at,
        })

    return result


@router.get("/pnl")
def pnl(db: Session = Depends(get_db)):
    positions = get_positions(db)

    unrealized = 0.0
    for pos in positions:
        current_price = get_price(pos.symbol)
        if current_price:
            unrealized += (current_price - pos.avg_price) * pos.qty

    portfolio = get_portfolio(db)
    initial_capital = 10_000.0
    realized = (
        portfolio.balance_usd - initial_capital
        if portfolio else 0.0
    )

    return {
        "realized_pnl": realized,
        "unrealized_pnl": unrealized,
        "total_pnl": realized + unrealized,
    }
