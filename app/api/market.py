from fastapi import FastAPI, Query, APIRouter, HTTPException
from app.market.symbol_service import load_symbols, search_symbols
from app.market.state import get_price
from app.market.subscription_manager import (
    subscribe,
    unsubscribe,
    list_subscriptions,
)


router = APIRouter(prefix="/market", tags=["market"])

@router.get("/symbols")
def get_symbols():
    """
    return all tradeable symbols
    """
    return {
        "count": len(load_symbols()),
        "symbols": load_symbols()
    }

@router.get("/symbols/search")
def search_symbol(q: str = Query(..., min_length=1, description="search querry")):
    """
    search symbol by name
    """
    results = search_symbols(q)
    return{
        "querry": q,
        "count": len(results),
        "results": results
    }

@router.get('/price/{symbol}')
def get_latest_price(symbol: str):
    price = get_price(symbol)
    if price is None:
        raise HTTPException(status_code=404, detail="price not found")
    return {
        "symbol" : symbol.upper(),
        "price": price
    }

@router.post("/subscribe/{symbol}")
async def subscribe_symbol(symbol: str):
    return await subscribe(symbol)

@router.post("/unsubscribe/{symbol}")
async def unsubscribe_symbol(symbol: str):
    return await unsubscribe(symbol)


@router.get("/subscriptions")
def active_subscriptions():
    return {"active": list_subscriptions()}