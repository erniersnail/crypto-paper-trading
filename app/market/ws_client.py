import asyncio
import websockets
import json
import logging
from app.market.state import set_price

logger = logging.getLogger(__name__)

def make_ws_url(symbol: str) -> str:
    return f"wss://stream.binance.com:9443/ws/{symbol.lower()}@trade"

async def binance_ws_listner(symbol: str, stop_event:asyncio.Event):
    """
    listens to binance websockets and updates the price
    """
    url = make_ws_url(symbol)
    while not stop_event.is_set():
        try:
            logger.info("connecting to binance")
            async with websockets.connect(
                url,
                ping_interval=20,
                ping_timeout=20
            ) as ws:
                logger.info("Connected to binance")
            async for message in ws:
                data = json.loads(message)
                price_str = data.get('p')
                if price_str is None:
                    continue
                price = float(price_str)
                symbol = str(symbol.upper())
                set_price(symbol, price)

        except Exception as e:
            logger.error("web connect error", exc_info=True)
            await asyncio.sleep(2) 



