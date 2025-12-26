import asyncio
from typing import Dict
from app.market.ws_client import binance_ws_listner

subscriptions: Dict[str, Dict] = {}

def is_subscribed(symbol:str) -> bool:
    return symbol.upper() in subscriptions

async def subscribe(symbol: str):
        symbol = symbol.upper()

        if is_subscribed(symbol):
            return {"status": "already subscribed", "symbol": symbol}
        
        stop_event = asyncio.Event()
        task = asyncio.create_task(binance_ws_listner(symbol, stop_event))

        subscriptions[symbol] = {
            'task': task,
            "event": stop_event
        }

        return {"status":"subscribed", "symbol":symbol}

async def unsubscribe(symbol:str):
        symbol = symbol.upper()

        if symbol not in subscriptions:
            return {"status":"not subscribed", "symbol": symbol}
        
        subscriptions[symbol]['event'].set()
        subscriptions[symbol]["task"].cancel()

        del subscriptions[symbol]

        return {"status": "unsubscribed", "symbol": symbol}

def list_subscriptions():
    return list(subscriptions.keys())