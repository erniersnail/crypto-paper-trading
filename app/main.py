# app/main.py

from fastapi import FastAPI
from app.api.market import router as market_router
from app.api.health import router as health_roter
from app.market.ws_client import binance_ws_listner
import asyncio
from app.api.trading import router as trading_router
from app.api.portfolio import router as portfolio_router

app = FastAPI(title="Crypto Paper Trading")

app.include_router(market_router)
app.include_router(health_roter)
app.include_router(trading_router)
app.include_router(portfolio_router)


