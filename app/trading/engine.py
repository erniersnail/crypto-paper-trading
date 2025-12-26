# app/trading/engine.py

from sqlalchemy.orm import Session

from app.db.models import OrderDB, TradeDB, PositionDB
from app.db.repository import get_or_create_portfolio, get_position
from app.market.state import get_price
from app.trading.risk import check_position_limit, required_margin


def execute_market_order(
    db: Session,
    symbol: str,
    side: str,
    qty: float,
):
    symbol = symbol.upper()
    side = side.upper()

    price = get_price(symbol)
    if price is None:
        raise ValueError("Market price not available")

    portfolio = get_or_create_portfolio(db)
    position = get_position(db, symbol)

    current_qty = position.qty if position else 0.0
    signed_qty = qty if side == "BUY" else -qty
    new_qty = current_qty + signed_qty

    # ---- RISK CHECKS ----
    check_position_limit(symbol, new_qty, price)

    margin_needed = required_margin(new_qty, price)
    if portfolio.balance_usd < margin_needed:
        raise ValueError("Insufficient margin")

    # ---- UPDATE POSITION ----
    if position:
        if new_qty == 0:
            db.delete(position)
        else:
            position.qty = new_qty
            position.avg_price = price
    else:
        position = PositionDB(
            symbol=symbol,
            qty=new_qty,
            avg_price=price,
        )
        db.add(position)

    # ---- CASH UPDATE ----
    trade_value = qty * price
    if side == "BUY":
        portfolio.balance_usd -= trade_value
    else:
        portfolio.balance_usd += trade_value

    # ---- ORDER & TRADE ----
    order = OrderDB(
        symbol=symbol,
        side=side,
        qty=qty,
        price=price,
        status="FILLED",
    )

    trade = TradeDB(
        order_id=None,
        symbol=symbol,
        side=side,
        qty=qty,
        price=price,
    )

    db.add(order)
    db.add(trade)
    db.commit()

    return {
        "symbol": symbol,
        "side": side,
        "qty": qty,
        "price": price,
        "position_qty": new_qty,
        "margin_used": margin_needed,
        "balance": portfolio.balance_usd,
    }
