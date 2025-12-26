MAX_POSITION_USD = 50_000     
MARGIN_RATE = 0.20

def check_position_limit(symbol: str, new_qty: float, price: float):
    exposure = abs(new_qty) * price
    if exposure > MAX_POSITION_USD:
        raise ValueError(
            f"Position limit exceeded for {symbol}: {exposure}"
        )

def required_margin(qty: float, price: float) -> float:
    return abs(qty) * price * MARGIN_RATE