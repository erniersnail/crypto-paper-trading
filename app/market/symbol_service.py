import requests
from difflib import get_close_matches

BINANCE_EXCHANGE_INFO_URL = "https://api.binance.com/api/v3/exchangeInfo"

_cached_symbols: set[str] = set()

def load_symbols(force_refresh: bool = False) -> list[str]:
    """
    Fetch all tradeable symbol from binance and cache them.
    """
    global _cached_symbols

    if _cached_symbols and not force_refresh:
        return sorted(_cached_symbols)
    
    response = requests.get(BINANCE_EXCHANGE_INFO_URL, timeout=10)
    response.raise_for_status()

    data = response.json()

    symbol = {
        s["symbol"] for s in data["symbols"] if s["status"] == "TRADING"
    }

    _cached_symbols = symbol

    return sorted(_cached_symbols)


def is_valid_symbol(symbol:str) -> bool:
    """
    Check if symbol exists in Binance trading symbol
    """
    if not _cached_symbols:
        load_symbols()
    
    return symbol.upper() in _cached_symbols

def search_symbols(querry: str, limit: int = 10) -> list[str]:
    """
    search symbols by substring or fuzzy match.
    """

    if not _cached_symbols:
        load_symbols()

    querry = querry.upper()

    matches = [s for s in _cached_symbols if querry in s]

    if matches:
        return sorted(matches)[:limit]
    
    return get_close_matches(querry, _cached_symbols, n=limit, cutoff=0.6)