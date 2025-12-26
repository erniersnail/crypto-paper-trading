# app/api/trading.py

from fastapi import APIRouter, Depends, HTTPException

from app.db.session import SessionLocal
from app.trading.services import place_order

router = APIRouter(prefix="/trade", tags=["trading"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/buy")
def buy(symbol: str, qty: float, db=Depends(get_db)):
    try:
        return place_order(db, symbol, "BUY", qty)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/sell")
def sell(symbol: str, qty: float, db=Depends(get_db)):
    try:
        return place_order(db, symbol, "SELL", qty)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
