# Crypto Paper Trading Backend

This project is a **paper trading backend for crypto markets** built from scratch to understand
how real trading systems are designed internally.

The goal was not to build a UI or a flashy product, but to focus on **backend architecture**:
live market data, async systems, risk-aware trade execution, and clean separation of concerns.

It simulates how an exchange or broker backend works, without using real money.

---

## Why I built this

Most tutorials show trading logic in a single file or mix WebSockets, APIs, and databases together.
I wanted to build this **slowly and correctly**, the way production systems are structured.

This project helped me deeply understand:
- Async WebSocket lifecycle management
- Real-time market data handling
- Trading engine design
- Risk management and margin logic
- Persistent trade and portfolio storage

---

## What this system does

- Connects to Binance WebSocket streams for live prices
- Supports subscribing and unsubscribing to multiple symbols
- Stores latest prices in Redis for fast access
- Executes paper BUY and SELL orders at market price
- Supports both **long and short positions**
- Enforces basic risk management (margin & position limits)
- Persists trades, positions, and portfolio state in PostgreSQL
- Exposes clean REST APIs to observe portfolio, trades, and PnL

---

## High-level architecture

