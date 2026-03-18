# BHARAT TERMINAL — Indian Markets Dashboard

A Bloomberg-style terminal for Indian markets — NSE, BSE, NIFTY, SENSEX, Commodities & MCX.
No paid API needed. All market data is free via Yahoo Finance.

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501

---

## Features

### Market Data (free, via yfinance)
- **NIFTY 50, SENSEX, BANK NIFTY, NIFTY IT, NIFTY MID** live in top bar
- **Watchlist** — pre-loaded with top NSE stocks, add any symbol
- **Charts** — Line / Candlestick / Area with volume bars
- **Time periods** — 1D · 1W · 1M · 3M · 6M · 1Y · 3Y
- **Key Metrics** — P/E, EPS, Market Cap, 52W High/Low, Beta, Dividend Yield, Volume
- **Sector Performance** — IT, Banking, Pharma, FMCG, Auto, Realty, Metal, Energy
- **Gainers & Losers** — live sorted from NIFTY 50 universe
- **Indices panel** — all major NSE indices
- **Commodities** — Gold, Silver, Crude Oil, Natural Gas, USD/INR
- **MCX Stocks** — Tata Steel, Hindalco, JSW Steel, ONGC, BPCL, IOC

### News (optional, requires NewsAPI key)
- Paste your free NewsAPI key (newsapi.org) in the sidebar
- News auto-filters to the currently selected stock

### Adding Stocks to Watchlist
Use Yahoo Finance symbol format:
- NSE stocks:  `BAJFINANCE.NS`, `HDFC.NS`, `ZOMATO.NS`
- BSE stocks:  `500325.BO`, `532540.BO`
- Indices:     `^NSEI`, `^BSESN`, `^CNXBANK`
- Commodities: `GC=F` (Gold), `CL=F` (Crude), `USDINR=X`

## Data Notes
- Yahoo Finance data has ~15min delay during market hours
- Cache TTL: 2 min for quotes, 5 min for news
- Click "Refresh Data" in bottom-right to force refresh
