from app.cache.redis_client import redis_client

PRICE_KEY_PREFIX = "price:"

def _key(symbol: str) -> str:
    return f"{PRICE_KEY_PREFIX}{symbol.upper()}"


def set_price(symbol: str, price: float) -> None:
    redis_client.set(_key(symbol), price)

def get_price(symbol: str) -> float | None:
    value = redis_client.get(_key(symbol))
    if value is None:
        return None
    return float(value)
