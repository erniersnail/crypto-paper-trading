
from sqlalchemy.orm import Session

from app.trading.engine import execute_market_order


def place_order(
    db: Session,
    symbol: str,
    side: str,
    qty: float,
):
    return execute_market_order(db, symbol, side, qty)
