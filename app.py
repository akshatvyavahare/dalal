import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import requests

# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Dalal Terminal", page_icon="◈", layout="wide",
                   initial_sidebar_state="collapsed")

# ─── MASTER NSE STOCK LIST ────────────────────────────────────────────────────
NSE_STOCKS = {
    "RELIANCE":    "Reliance Industries",
    "TCS":         "Tata Consultancy Services",
    "HDFCBANK":    "HDFC Bank",
    "INFY":        "Infosys",
    "ICICIBANK":   "ICICI Bank",
    "HINDUNILVR":  "Hindustan Unilever",
    "ITC":         "ITC Limited",
    "SBIN":        "State Bank of India",
    "BHARTIARTL":  "Bharti Airtel",
    "KOTAKBANK":   "Kotak Mahindra Bank",
    "LT":          "Larsen & Toubro",
    "AXISBANK":    "Axis Bank",
    "ASIANPAINT":  "Asian Paints",
    "MARUTI":      "Maruti Suzuki",
    "TITAN":       "Titan Company",
    "WIPRO":       "Wipro",
    "BAJFINANCE":  "Bajaj Finance",
    "NESTLEIND":   "Nestle India",
    "ULTRACEMCO":  "UltraTech Cement",
    "TECHM":       "Tech Mahindra",
    "SUNPHARMA":   "Sun Pharmaceutical",
    "HCLTECH":     "HCL Technologies",
    "POWERGRID":   "Power Grid Corp",
    "NTPC":        "NTPC Limited",
    "TATAMOTORS":  "Tata Motors",
    "TATASTEEL":   "Tata Steel",
    "HINDALCO":    "Hindalco Industries",
    "JSWSTEEL":    "JSW Steel",
    "ONGC":        "Oil & Natural Gas Corp",
    "BPCL":        "Bharat Petroleum",
    "IOC":         "Indian Oil Corporation",
    "COALINDIA":   "Coal India",
    "GRASIM":      "Grasim Industries",
    "ADANIENT":    "Adani Enterprises",
    "ADANIPORTS":  "Adani Ports",
    "ADANIGREEN":  "Adani Green Energy",
    "AMBUJACEM":   "Ambuja Cements",
    "APOLLOHOSP":  "Apollo Hospitals",
    "BAJAJFINSV":  "Bajaj Finserv",
    "BAJAJ-AUTO":  "Bajaj Auto",
    "BANDHANBNK":  "Bandhan Bank",
    "BERGEPAINT":  "Berger Paints",
    "BIOCON":      "Biocon",
    "BOSCHLTD":    "Bosch",
    "BRITANNIA":   "Britannia Industries",
    "CANBK":       "Canara Bank",
    "CHOLAFIN":    "Cholamandalam Finance",
    "CIPLA":       "Cipla",
    "COLPAL":      "Colgate-Palmolive India",
    "DABUR":       "Dabur India",
    "DIVISLAB":    "Divi's Laboratories",
    "DLF":         "DLF",
    "DRREDDY":     "Dr. Reddy's Laboratories",
    "EICHERMOT":   "Eicher Motors",
    "FEDERALBNK":  "Federal Bank",
    "GAIL":        "GAIL India",
    "GODREJCP":    "Godrej Consumer Products",
    "GODREJPROP":  "Godrej Properties",
    "HDFCAMC":     "HDFC AMC",
    "HDFCLIFE":    "HDFC Life Insurance",
    "HEROMOTOCO":  "Hero MotoCorp",
    "HINDZINC":    "Hindustan Zinc",
    "IDFCFIRSTB":  "IDFC First Bank",
    "INDHOTEL":    "Indian Hotels",
    "INDIGO":      "IndiGo (InterGlobe Aviation)",
    "INDUSINDBK":  "IndusInd Bank",
    "INDUSTOWER":  "Indus Towers",
    "IRCTC":       "IRCTC",
    "JSWENERGY":   "JSW Energy",
    "JUBLFOOD":    "Jubilant FoodWorks",
    "LICI":        "LIC India",
    "LTIM":        "LTIMindtree",
    "LUPIN":       "Lupin",
    "M&M":         "Mahindra & Mahindra",
    "MARICO":      "Marico",
    "MPHASIS":     "Mphasis",
    "MRF":         "MRF",
    "MUTHOOTFIN":  "Muthoot Finance",
    "NAUKRI":      "Info Edge (Naukri)",
    "NMDC":        "NMDC",
    "OBEROIRLTY":  "Oberoi Realty",
    "OFSS":        "Oracle Financial Services",
    "PAGEIND":     "Page Industries",
    "PERSISTENT":  "Persistent Systems",
    "PETRONET":    "Petronet LNG",
    "PFC":         "Power Finance Corp",
    "PIDILITIND":  "Pidilite Industries",
    "PNB":         "Punjab National Bank",
    "POLYCAB":     "Polycab India",
    "RECLTD":      "REC Limited",
    "SAIL":        "Steel Authority of India",
    "SHREECEM":    "Shree Cement",
    "SIEMENS":     "Siemens India",
    "SRF":         "SRF Limited",
    "SRTRANSFIN":  "Shriram Finance",
    "TATACOMM":    "Tata Communications",
    "TATACONSUM":  "Tata Consumer Products",
    "TATAELXSI":   "Tata Elxsi",
    "TATAPOWER":   "Tata Power",
    "TORNTPHARM":  "Torrent Pharmaceuticals",
    "TORNTPOWER":  "Torrent Power",
    "TRENT":       "Trent",
    "TVSMOTOR":    "TVS Motor Company",
    "UBL":         "United Breweries",
    "UNIONBANK":   "Union Bank of India",
    "UPL":         "UPL",
    "VEDL":        "Vedanta",
    "VOLTAS":      "Voltas",
    "YESBANK":     "Yes Bank",
    "ZOMATO":      "Zomato",
    "PAYTM":       "One97 Communications (Paytm)",
    "NYKAA":       "FSN E-Commerce (Nykaa)",
    "DELHIVERY":   "Delhivery",
    "POLICYBZR":   "PB Fintech (PolicyBazaar)",
    "MANKIND":     "Mankind Pharma",
    "MAPMYINDIA":  "MapmyIndia",
    "KAYNES":      "Kaynes Technology",
    "PIIND":       "PI Industries",
    "BALKRISIND":  "Balkrishna Industries",
    "DEEPAKNTR":   "Deepak Nitrite",
    "FLUOROCHEM":  "Gujarat Fluorochemicals",
    "GMRAIRPORT":  "GMR Airports",
    "GUJGASLTD":   "Gujarat Gas",
    "HAL":         "Hindustan Aeronautics",
    "HAVELLS":     "Havells India",
    "HFCL":        "HFCL",
    "HUDCO":       "HUDCO",
    "ICICIGI":     "ICICI Lombard",
    "ICICIPRULI":  "ICICI Prudential Life",
    "INDIANB":     "Indian Bank",
    "INOXWIND":    "INOX Wind",
    "IRFC":        "Indian Railway Finance Corp",
    "JKCEMENT":    "JK Cement",
    "JUBILEE":     "Jubilant Pharmova",
    "KPITTECH":    "KPIT Technologies",
    "LICHSGFIN":   "LIC Housing Finance",
    "LINDEINDIA":  "Linde India",
    "LODHA":       "Macrotech Developers (Lodha)",
    "LTTS":        "L&T Technology Services",
    "MAXHEALTH":   "Max Healthcare",
    "MCX":         "Multi Commodity Exchange",
    "MEDANTA":     "Global Health (Medanta)",
    "MOTHERSUMI":  "Motherson Sumi Wiring",
    "MFSL":        "Max Financial Services",
    "NH":          "Narayana Hrudayalaya",
    "NLCINDIA":    "NLC India",
    "NSLNISP":     "NMDC Steel",
    "OLECTRA":     "Olectra Greentech",
    "PCBL":        "PCBL",
    "PGHH":        "Procter & Gamble Hygiene",
    "PHOENIXLTD":  "Phoenix Mills",
    "PRESTIGE":    "Prestige Estates",
    "PRINCEPIPE":  "Prince Pipes",
    "PVR":         "PVR INOX",
    "RAINBOW":     "Rainbow Childrens Medicare",
    "RAMCOCEM":    "Ramco Cements",
    "RBLBANK":     "RBL Bank",
    "RITES":       "RITES",
    "ROUTE":       "Route Mobile",
    "SAFARI":      "Safari Industries",
    "SCHAEFFLER":  "Schaeffler India",
    "SHYAMMETL":   "Shyam Metalics",
    "SOBHA":       "Sobha",
    "STARHEALTH":  "Star Health Insurance",
    "SUNDARMFIN":  "Sundaram Finance",
    "SUPREMEIND":  "Supreme Industries",
    "SUVENPHAR":   "Suven Pharmaceuticals",
    "TANLA":       "Tanla Platforms",
    "THERMAX":     "Thermax",
    "TIINDIA":     "Tube Investments",
    "TRIDENT":     "Trident",
    "TRITURBINE":  "Triveni Turbine",
    "VBL":         "Varun Beverages",
    "VINATIORGA":  "Vinati Organics",
    "WELCORP":     "Welspun Corp",
    "WHIRLPOOL":   "Whirlpool India",
    "ZEEL":        "Zee Entertainment",
    "ZYDUSLIFE":   "Zydus Lifesciences",
}

INDICES = [
    {"sym": "^NSEI",    "name": "NIFTY 50"},
    {"sym": "^BSESN",   "name": "SENSEX"},
    {"sym": "^NSMIDCP", "name": "NIFTY MID"},
    {"sym": "^CNXIT",   "name": "NIFTY IT"},
    {"sym": "^CNXBANK", "name": "BANK NIFTY"},
]
COMMODITIES = [
    {"sym": "GC=F",     "name": "Gold"},
    {"sym": "SI=F",     "name": "Silver"},
    {"sym": "CL=F",     "name": "Crude Oil"},
    {"sym": "NG=F",     "name": "Natural Gas"},
    {"sym": "USDINR=X", "name": "USD/INR"},
    {"sym": "EURINR=X", "name": "EUR/INR"},
    {"sym": "GBPINR=X", "name": "GBP/INR"},
    {"sym": "JPYINR=X", "name": "JPY/INR"},
]
MCX_LIST = [
    {"sym": "TATASTEEL.NS", "name": "Tata Steel"},
    {"sym": "HINDALCO.NS",  "name": "Hindalco"},
    {"sym": "JSWSTEEL.NS",  "name": "JSW Steel"},
    {"sym": "VEDL.NS",      "name": "Vedanta"},
    {"sym": "NMDC.NS",      "name": "NMDC"},
    {"sym": "SAIL.NS",      "name": "SAIL"},
    {"sym": "HINDZINC.NS",  "name": "Hindustan Zinc"},
    {"sym": "ONGC.NS",      "name": "ONGC"},
    {"sym": "BPCL.NS",      "name": "BPCL"},
    {"sym": "IOC.NS",       "name": "Indian Oil"},
    {"sym": "GAIL.NS",      "name": "GAIL"},
    {"sym": "PETRONET.NS",  "name": "Petronet LNG"},
    {"sym": "MCX.NS",       "name": "MCX India"},
]
SECTOR_INDICES = [
    {"sym": "^CNXIT",       "name": "IT"},
    {"sym": "^CNXBANK",     "name": "Banking"},
    {"sym": "^CNXPHARMA",   "name": "Pharma"},
    {"sym": "^CNXFMCG",     "name": "FMCG"},
    {"sym": "^CNXAUTO",     "name": "Auto"},
    {"sym": "^CNXREALTY",   "name": "Realty"},
    {"sym": "^CNXMETAL",    "name": "Metal"},
    {"sym": "^CNXENERGY",   "name": "Energy"},
]
NIFTY50_SYMS = [k + ".NS" for k in [
    "RELIANCE","TCS","HDFCBANK","INFY","ICICIBANK","HINDUNILVR","ITC","SBIN",
    "BHARTIARTL","KOTAKBANK","LT","AXISBANK","ASIANPAINT","MARUTI","TITAN",
    "WIPRO","BAJFINANCE","NESTLEIND","ULTRACEMCO","TECHM","SUNPHARMA","HCLTECH",
    "POWERGRID","NTPC","TATAMOTORS","HINDALCO","JSWSTEEL","ONGC","BPCL","COALINDIA",
    "GRASIM","ADANIENT","ADANIPORTS","TATASTEEL","BAJAJFINSV","BAJAJ-AUTO",
    "DIVISLAB","DRREDDY","EICHERMOT","HEROMOTOCO","INDUSINDBK","M&M",
    "TATACONSUM","TATAPOWER","TRENT","UPL","VEDL","BRITANNIA","CIPLA","LUPIN",
]]
PERIODS = {
    "1D":  ("1d",  "5m"),
    "1W":  ("5d",  "15m"),
    "1M":  ("1mo", "1h"),
    "3M":  ("3mo", "1d"),
    "6M":  ("6mo", "1d"),
    "1Y":  ("1y",  "1d"),
    "3Y":  ("3y",  "1wk"),
}

# ─── SESSION STATE ─────────────────────────────────────────────────────────────
def ss(k, v):
    if k not in st.session_state: st.session_state[k] = v

ss("watchlist", [
    {"sym": "RELIANCE.NS",  "name": "Reliance Industries"},
    {"sym": "TCS.NS",       "name": "Tata Consultancy Services"},
    {"sym": "HDFCBANK.NS",  "name": "HDFC Bank"},
    {"sym": "INFY.NS",      "name": "Infosys"},
    {"sym": "ICICIBANK.NS", "name": "ICICI Bank"},
    {"sym": "SBIN.NS",      "name": "State Bank of India"},
    {"sym": "TATAMOTORS.NS","name": "Tata Motors"},
    {"sym": "WIPRO.NS",     "name": "Wipro"},
])
ss("sel_sym",    "RELIANCE.NS")
ss("sel_name",   "Reliance Industries")
ss("period",     "1M")
ss("chart_type", "Candle")
ss("right_tab",  "Gainers")
ss("news_key",   "")
ss("ctab",       "Overview")

# ─── DATA HELPERS ─────────────────────────────────────────────────────────────
def to_yf_sym(raw):
    raw = raw.strip().upper()
    if any(raw.endswith(s) for s in [".NS",".BO","=F","=X"]) or raw.startswith("^"):
        return raw
    return raw + ".NS"

@st.cache_data(ttl=120, show_spinner=False)
def get_quote(sym):
    try:
        fi = yf.Ticker(sym).fast_info
        price = round(float(fi.last_price or 0), 2)
        prev  = round(float(fi.previous_close or 0), 2)
        chg   = round(price - prev, 2)
        pct   = round((chg / prev * 100) if prev else 0, 2)
        hi    = round(float(fi.day_high or 0), 2)
        lo    = round(float(fi.day_low  or 0), 2)
        return {"price": price, "prev": prev, "chg": chg, "pct": pct, "hi": hi, "lo": lo}
    except:
        return {"price": 0, "prev": 0, "chg": 0, "pct": 0, "hi": 0, "lo": 0}

@st.cache_data(ttl=300, show_spinner=False)
def get_info(sym):
    try: return yf.Ticker(sym).info or {}
    except: return {}

@st.cache_data(ttl=180, show_spinner=False)
def get_hist(sym, period, interval):
    try:
        df = yf.download(sym, period=period, interval=interval,
                         progress=False, auto_adjust=True)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        return df.dropna(how="all")
    except:
        return pd.DataFrame()

@st.cache_data(ttl=300, show_spinner=False)
def get_financials(sym):
    try:
        t = yf.Ticker(sym)
        return t.financials, t.balance_sheet, t.cashflow
    except:
        return None, None, None

@st.cache_data(ttl=300, show_spinner=False)
def fetch_news(api_key, query):
    if not api_key: return []
    try:
        r = requests.get("https://newsapi.org/v2/everything", params={
            "q": query, "apiKey": api_key, "sortBy": "publishedAt",
            "pageSize": 15, "language": "en",
        }, timeout=8)
        d = r.json()
        return d.get("articles", []) if d.get("status") == "ok" else []
    except: return []

def time_ago(s):
    try:
        dt = datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
        d  = int((datetime.utcnow() - dt).total_seconds())
        if d < 3600:  return f"{d//60}m ago"
        if d < 86400: return f"{d//3600}h ago"
        return f"{d//86400}d ago"
    except: return ""

def fmt_inr(v):
    try:
        v = float(v)
        if v == 0: return "—"
        if v >= 1e12: return f"₹{v/1e12:.2f}T"
        if v >= 1e9:  return f"₹{v/1e9:.2f}B"
        if v >= 1e7:  return f"₹{v/1e7:.2f}Cr"
        if v >= 1e5:  return f"₹{v/1e5:.2f}L"
        return f"₹{v:,.2f}"
    except: return "—"

def safe(v, prefix="₹", suffix="", dec=2, fmt=None):
    if v is None: return "—"
    try:
        f = float(v)
        if f == 0: return "—"
        if fmt == "pct": return f"{f*100:.{dec}f}%"
        if fmt == "vol":
            if f >= 1e7: return f"{f/1e7:.2f}Cr"
            if f >= 1e5: return f"{f/1e5:.2f}L"
            return f"{int(f):,}"
        if fmt == "cr": return fmt_inr(f)
        return f"{prefix}{f:,.{dec}f}{suffix}"
    except: return "—"

def ud(pct):
    return ("▲", "#22c55e") if pct >= 0 else ("▼", "#ef4444")

def search_stocks(q):
    q = q.strip().upper()
    if not q or len(q) < 2: return []
    return [{"sym": k, "name": v}
            for k, v in NSE_STOCKS.items()
            if q in k or q in v.upper()][:8]

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600&family=Outfit:wght@300;400;500;600&display=swap');
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body,[class*="css"]{font-family:'Outfit',sans-serif;background:#07090e;color:#e2e8f0}
.main .block-container{padding:0!important;max-width:100%!important}
section[data-testid="stSidebar"]{display:none!important}
#MainMenu,footer,header,[data-testid="stToolbar"],.stDeployButton{display:none!important}
::-webkit-scrollbar{width:3px;background:transparent}
::-webkit-scrollbar-thumb{background:#1e2535;border-radius:2px}

/* TOPBAR */
.topbar{display:flex;align-items:center;padding:0 20px;height:50px;
  background:#0b0d16;border-bottom:1px solid #161c2d;gap:14px;
  position:sticky;top:0;z-index:100;overflow-x:auto}
.t-logo{font-family:'JetBrains Mono',monospace;font-size:0.85rem;font-weight:600;
  color:#f97316;letter-spacing:0.22em;white-space:nowrap;padding-right:6px}
.idx-pill{display:flex;flex-direction:column;padding:4px 12px;border-radius:5px;
  background:#10131e;border:1px solid #1c2238;min-width:96px;cursor:default}
.idx-n{font-family:'JetBrains Mono',monospace;font-size:0.52rem;color:#475569;
  letter-spacing:0.1em;text-transform:uppercase}
.idx-v{font-family:'JetBrains Mono',monospace;font-size:0.78rem;font-weight:500;color:#f1f5f9}
.idx-c{font-family:'JetBrains Mono',monospace;font-size:0.6rem}
.g{color:#22c55e}.r{color:#ef4444}
.t-time{margin-left:auto;font-family:'JetBrains Mono',monospace;font-size:0.58rem;color:#2d3f5c;white-space:nowrap}
.t-live{font-family:'JetBrains Mono',monospace;font-size:0.58rem;color:#22c55e;
  border:1px solid #22c55e44;padding:2px 8px;border-radius:3px;white-space:nowrap}

/* COLUMNS */
div[data-testid="column"]:nth-child(1){padding-right:0!important}
div[data-testid="column"]:nth-child(3){padding-left:0!important}

/* SECTION HEADER */
.sh{font-family:'JetBrains Mono',monospace;font-size:0.56rem;color:#334155;
  letter-spacing:0.14em;text-transform:uppercase;padding:9px 12px 7px;
  border-bottom:1px solid #10131e;background:#0b0d16}

/* WATCHLIST BUTTONS — OVERRIDE STREAMLIT */
.stButton>button{
  font-family:'JetBrains Mono',monospace!important;
  font-size:0.68rem!important;border-radius:3px!important;
  padding:6px 10px!important;width:100%!important;
  text-align:left!important;transition:all 0.12s!important;
  letter-spacing:0.01em!important;
  background:#10131e!important;color:#94a3b8!important;
  border:1px solid #1c2238!important;
}
.stButton>button:hover{
  background:#14182a!important;color:#f1f5f9!important;
  border-color:#2d3f5c!important
}
.stButton>button[kind="primary"]{
  background:#f97316!important;color:#07090e!important;
  border-color:#f97316!important;font-weight:600!important;
  color:#07090e!important
}

/* TEXT INPUT */
.stTextInput>div>div>input{
  background:#10131e!important;border:1px solid #1c2238!important;
  color:#e2e8f0!important;border-radius:4px!important;
  font-family:'JetBrains Mono',monospace!important;font-size:0.7rem!important;
  padding:7px 10px!important
}
.stTextInput>div>div>input:focus{border-color:#f97316!important;box-shadow:none!important}
.stTextInput>div>div>input::placeholder{color:#334155!important}
.stTextInput label,.stTextInput [data-testid="stWidgetLabel"]{
  font-family:'JetBrains Mono',monospace!important;font-size:0.55rem!important;
  color:#334155!important;text-transform:uppercase!important;letter-spacing:0.1em!important
}

/* EXPANDER */
.streamlit-expanderHeader{
  font-family:'JetBrains Mono',monospace!important;font-size:0.62rem!important;
  color:#475569!important;background:#0b0d16!important;
  border:1px solid #161c2d!important
}

/* STOCK BANNER */
.banner{background:#0b0d16;border:1px solid #161c2d;border-radius:7px;
  padding:16px 18px;margin-bottom:12px}
.b-name{font-size:1rem;font-weight:600;color:#f8fafc;line-height:1}
.b-sym{font-family:'JetBrains Mono',monospace;font-size:0.6rem;color:#475569;margin-top:4px}
.b-price{font-family:'JetBrains Mono',monospace;font-size:1.85rem;font-weight:600;
  color:#f8fafc;line-height:1;text-align:right}
.b-chg{font-family:'JetBrains Mono',monospace;font-size:0.8rem;margin-top:5px;text-align:right}
.ohlc{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px}
.ohlc-p{background:#10131e;border:1px solid #1c2238;border-radius:4px;
  padding:3px 10px;font-family:'JetBrains Mono',monospace;font-size:0.63rem}
.ol{color:#475569;margin-right:3px}
.ov{color:#e2e8f0;font-weight:500}
.ov-g{color:#22c55e;font-weight:500}
.ov-r{color:#ef4444;font-weight:500}

/* SECTION TITLE */
.st2{font-family:'JetBrains Mono',monospace;font-size:0.57rem;color:#334155;
  letter-spacing:0.14em;text-transform:uppercase;padding:10px 0 8px;
  border-bottom:1px solid #10131e;margin-bottom:12px}

/* METRIC CARD */
.mc{background:#0b0d16;border:1px solid #161c2d;border-radius:5px;padding:9px 11px}
.ml{font-family:'JetBrains Mono',monospace;font-size:0.52rem;color:#334155;
  text-transform:uppercase;letter-spacing:0.1em}
.mv{font-family:'JetBrains Mono',monospace;font-size:0.82rem;font-weight:500;
  color:#f1f5f9;margin-top:4px}
.mv-g{font-family:'JetBrains Mono',monospace;font-size:0.82rem;font-weight:500;
  color:#22c55e;margin-top:4px}
.mv-r{font-family:'JetBrains Mono',monospace;font-size:0.82rem;font-weight:500;
  color:#ef4444;margin-top:4px}

/* FUNDAMENTALS TABLE */
.ft{width:100%;border-collapse:collapse}
.ft td{padding:6px 10px;border-bottom:1px solid #0f1220;font-size:0.72rem}
.ft tr:hover td{background:#0b0d16}
.ft .fl{color:#475569;font-family:'JetBrains Mono',monospace;font-size:0.6rem;text-transform:uppercase}
.ft .fv{color:#e2e8f0;text-align:right;font-family:'JetBrains Mono',monospace;font-size:0.72rem}

/* NEWS */
.nc{padding:8px 12px;border-bottom:1px solid #0e1120;transition:background 0.1s;cursor:pointer}
.nc:hover{background:#10131e}
.ns{font-family:'JetBrains Mono',monospace;font-size:0.54rem;color:#f97316;
  text-transform:uppercase;letter-spacing:0.08em}
.nt{font-size:0.68rem;color:#94a3b8;line-height:1.4;margin-top:2px}
.nd{font-family:'JetBrains Mono',monospace;font-size:0.54rem;color:#1e3a5f;margin-top:3px}

/* SEARCH RESULTS */
.sr{background:#10131e;border:1px solid #1c2238;border-radius:4px;margin-top:2px}
.sr-row{padding:6px 10px;cursor:pointer;border-bottom:1px solid #161c2d;transition:background 0.1s}
.sr-row:last-child{border-bottom:none}
.sr-row:hover{background:#161c2d}
.sr-sym{font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:#f97316;font-weight:500}
.sr-nm{font-size:0.62rem;color:#475569}

/* SECTOR TILE */
.sectile{background:#0b0d16;border:1px solid #161c2d;border-radius:5px;
  padding:9px;text-align:center}
.secn{font-family:'JetBrains Mono',monospace;font-size:0.55rem;color:#334155;
  text-transform:uppercase;letter-spacing:0.08em}
.secp{font-family:'JetBrains Mono',monospace;font-size:0.82rem;font-weight:600;margin-top:4px}

/* DATAFRAME OVERRIDES */
.stDataFrame{border:1px solid #161c2d!important;border-radius:5px!important}
[data-testid="stPlotlyChart"]{border-radius:6px;overflow:hidden}
</style>
""", unsafe_allow_html=True)

# ─── TOPBAR ───────────────────────────────────────────────────────────────────
idx_quotes = {i["sym"]: get_quote(i["sym"]) for i in INDICES}
chips = ""
for i in INDICES:
    q = idx_quotes[i["sym"]]
    arr, col = ud(q["pct"])
    cc = "g" if q["pct"] >= 0 else "r"
    chips += f"""<div class="idx-pill">
      <span class="idx-n">{i['name']}</span>
      <span class="idx-v">{q['price']:,.2f}</span>
      <span class="idx-c {cc}">{arr} {abs(q['pct']):.2f}%</span>
    </div>"""
now_str = datetime.now().strftime("%d %b %Y  %H:%M IST")
st.markdown(f"""<div class="topbar">
  <span class="t-logo">◈ DALAL</span>
  {chips}
  <span class="t-time">{now_str}</span>
  <span class="t-live">● LIVE</span>
</div>""", unsafe_allow_html=True)

# ─── LAYOUT ───────────────────────────────────────────────────────────────────
L, C, R = st.columns([2.2, 6.2, 2.6])

# ══════════════ LEFT ══════════════════════════════════════════════════════════
with L:
    # Search
    st.markdown('<div class="sh">Search & Add</div>', unsafe_allow_html=True)
    raw_q = st.text_input("", placeholder="e.g. SBIN or State Bank...",
                          key="sq", label_visibility="collapsed")
    results = search_stocks(raw_q) if raw_q else []
    if results:
        st.markdown('<div class="sr">', unsafe_allow_html=True)
        for r in results:
            ca, cb = st.columns([4, 1])
            with ca:
                st.markdown(f"""<div class="sr-row">
                  <div class="sr-sym">{r['sym']}</div>
                  <div class="sr-nm">{r['name']}</div>
                </div>""", unsafe_allow_html=True)
            with cb:
                if st.button("＋", key=f"a_{r['sym']}"):
                    e = {"sym": r["sym"] + ".NS", "name": r["name"]}
                    if e not in st.session_state.watchlist:
                        st.session_state.watchlist.append(e)
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with st.expander("Add by full ticker (e.g. SBIN.NS)"):
        mt = st.text_input("", placeholder="SBIN.NS or SBIN", key="mt",
                           label_visibility="collapsed")
        if st.button("Add", key="btn_add_manual"):
            if mt.strip():
                sym = to_yf_sym(mt)
                base = mt.strip().upper().replace(".NS","").replace(".BO","")
                nm   = NSE_STOCKS.get(base, base)
                e    = {"sym": sym, "name": nm}
                if e not in st.session_state.watchlist:
                    st.session_state.watchlist.append(e)
                st.rerun()

    # Watchlist
    st.markdown('<div class="sh">Watchlist</div>', unsafe_allow_html=True)
    to_remove = None
    for i, w in enumerate(st.session_state.watchlist):
        q    = get_quote(w["sym"])
        base = w["sym"].replace(".NS","").replace(".BO","")
        arr, col = ud(q["pct"])
        p_s  = f"₹{q['price']:,.2f}" if q["price"] else "—"
        pcs  = f"{arr}{abs(q['pct']):.2f}%"
        is_s = w["sym"] == st.session_state.sel_sym
        c1, c2 = st.columns([5, 1])
        with c1:
            tp = "primary" if is_s else "secondary"
            if st.button(f"{base}  {p_s}  {pcs}", key=f"ws_{i}", type=tp):
                st.session_state.sel_sym  = w["sym"]
                st.session_state.sel_name = w["name"]
                st.rerun()
        with c2:
            if st.button("✕", key=f"wd_{i}"):
                to_remove = i
    if to_remove is not None:
        st.session_state.watchlist.pop(to_remove)
        syms = [w["sym"] for w in st.session_state.watchlist]
        if st.session_state.sel_sym not in syms and syms:
            st.session_state.sel_sym  = st.session_state.watchlist[0]["sym"]
            st.session_state.sel_name = st.session_state.watchlist[0]["name"]
        st.rerun()

    # News
    st.markdown('<div class="sh">News Feed</div>', unsafe_allow_html=True)
    nk = st.text_input("", type="password", placeholder="NewsAPI key (newsapi.org)…",
                       key="nk", label_visibility="collapsed")
    if nk: st.session_state.news_key = nk

    arts = fetch_news(st.session_state.news_key, f"India NSE BSE {st.session_state.sel_name}")
    if arts:
        for a in arts[:12]:
            src = (a.get("source",{}).get("name",""))[:20]
            ttl = (a.get("title",""))[:72]
            pub = a.get("publishedAt","")
            url = a.get("url","#")
            st.markdown(f"""<div class="nc" onclick="window.open('{url}','_blank')">
              <div class="ns">{src}</div>
              <div class="nt">{ttl}</div>
              <div class="nd">{time_ago(pub)}</div>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div style="padding:10px 12px;font-size:0.62rem;color:#1e3a5f;font-family:JetBrains Mono,monospace">Paste NewsAPI key above for live news</div>', unsafe_allow_html=True)


# ══════════════ CENTER ════════════════════════════════════════════════════════
with C:
    q    = get_quote(st.session_state.sel_sym)
    info = get_info(st.session_state.sel_sym)
    arr, col = ud(q["pct"])

    # OHLC values
    p       = q["price"]
    chg     = q["chg"]
    pct     = q["pct"]
    hi      = q["hi"] or info.get("dayHigh") or info.get("regularMarketDayHigh") or 0
    lo      = q["lo"] or info.get("dayLow")  or info.get("regularMarketDayLow")  or 0
    op_     = info.get("open") or info.get("regularMarketOpen") or 0
    pc      = q["prev"] or info.get("previousClose") or 0

    # Banner
    st.markdown(f"""<div class="banner">
      <div style="display:flex;justify-content:space-between;align-items:flex-start">
        <div>
          <div class="b-name">{st.session_state.sel_name}</div>
          <div class="b-sym">{st.session_state.sel_sym} · NSE/BSE</div>
          <div class="ohlc">
            <div class="ohlc-p"><span class="ol">O</span><span class="ov">{'₹'+f'{op_:,.2f}' if op_ else '—'}</span></div>
            <div class="ohlc-p"><span class="ol">H</span><span class="ov-g">{'₹'+f'{hi:,.2f}' if hi else '—'}</span></div>
            <div class="ohlc-p"><span class="ol">L</span><span class="ov-r">{'₹'+f'{lo:,.2f}' if lo else '—'}</span></div>
            <div class="ohlc-p"><span class="ol">PC</span><span class="ov">{'₹'+f'{pc:,.2f}' if pc else '—'}</span></div>
          </div>
        </div>
        <div>
          <div class="b-price">{'₹'+f'{p:,.2f}' if p else '—'}</div>
          <div class="b-chg" style="color:{col}">{arr} ₹{abs(chg):,.2f} ({abs(pct):.2f}%)</div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    # Period + chart type
    all_btns = list(PERIODS.keys()) + ["Line", "Candle", "Area"]
    p_cols   = st.columns(len(all_btns))
    for i, lbl in enumerate(list(PERIODS.keys())):
        tp = "primary" if st.session_state.period == lbl else "secondary"
        if p_cols[i].button(lbl, key=f"pb_{lbl}", type=tp):
            st.session_state.period = lbl; st.rerun()
    for j, ct in enumerate(["Line", "Candle", "Area"]):
        tp = "primary" if st.session_state.chart_type == ct else "secondary"
        if p_cols[len(PERIODS)+j].button(ct, key=f"cb_{ct}", type=tp):
            st.session_state.chart_type = ct; st.rerun()

    # Chart
    pr, iv = PERIODS[st.session_state.period]
    df     = get_hist(st.session_state.sel_sym, pr, iv)
    is_pos = pct >= 0
    up_c, dn_c = "#22c55e", "#ef4444"
    lc = up_c if is_pos else dn_c
    fa = "rgba(34,197,94,0.06)" if is_pos else "rgba(239,68,68,0.06)"

    if not df.empty and "Close" in df.columns:
        has_ohlc = all(c in df.columns for c in ["Open","High","Low","Close"])

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                            row_heights=[0.73, 0.27], vertical_spacing=0.015)

        ct = st.session_state.chart_type
        if ct == "Candle" and has_ohlc:
            fig.add_trace(go.Candlestick(
                x=df.index, open=df["Open"], high=df["High"],
                low=df["Low"], close=df["Close"],
                increasing=dict(line_color=up_c, fillcolor=up_c + "bb"),
                decreasing=dict(line_color=dn_c, fillcolor=dn_c + "bb"),
                line_width=1, name="OHLC", showlegend=False,
            ), row=1, col=1)
        elif ct == "Area":
            fig.add_trace(go.Scatter(
                x=df.index, y=df["Close"], mode="lines",
                line=dict(color=lc, width=1.5),
                fill="tozeroy", fillcolor=fa, name="Price", showlegend=False,
            ), row=1, col=1)
        else:
            fig.add_trace(go.Scatter(
                x=df.index, y=df["Close"], mode="lines",
                line=dict(color=lc, width=1.5), name="Price", showlegend=False,
            ), row=1, col=1)

        # MA overlays
        if len(df) >= 20:
            fig.add_trace(go.Scatter(
                x=df.index, y=df["Close"].rolling(20).mean(),
                mode="lines", line=dict(color="#f59e0b", width=1, dash="dot"),
                name="MA20", opacity=0.8), row=1, col=1)
        if len(df) >= 50:
            fig.add_trace(go.Scatter(
                x=df.index, y=df["Close"].rolling(50).mean(),
                mode="lines", line=dict(color="#818cf8", width=1, dash="dot"),
                name="MA50", opacity=0.8), row=1, col=1)

        # Volume
        if "Volume" in df.columns:
            vcols = [up_c if (c >= o) else dn_c
                     for c, o in zip(df["Close"], df.get("Open", df["Close"]))]
            fig.add_trace(go.Bar(
                x=df.index, y=df["Volume"], marker_color=vcols,
                opacity=0.45, name="Vol", showlegend=False), row=2, col=1)

        axis_style = dict(showgrid=False, zeroline=False, color="#334155",
                          tickfont=dict(family="JetBrains Mono", size=10, color="#334155"))
        yax_style  = dict(showgrid=True, gridcolor="#0f1220", zeroline=False,
                          side="right", color="#334155",
                          tickfont=dict(family="JetBrains Mono", size=10, color="#334155"))

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=4, t=4, b=0), height=340,
            showlegend=True,
            legend=dict(orientation="h", y=1.04, x=0, font=dict(
                family="JetBrains Mono", size=10, color="#475569"),
                bgcolor="rgba(0,0,0,0)"),
            hovermode="x unified",
            hoverlabel=dict(bgcolor="#10131e", bordercolor="#1c2238",
                            font=dict(family="JetBrains Mono", size=11, color="#e2e8f0")),
            xaxis=dict(**axis_style),
            xaxis2=dict(**axis_style, rangeslider=dict(visible=False)),
            yaxis=dict(**yax_style),
            yaxis2=dict(showgrid=False, showticklabels=False),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.markdown('<div style="height:280px;display:flex;align-items:center;justify-content:center;color:#1e3a5f;font-family:JetBrains Mono,monospace;font-size:0.72rem;border:1px solid #161c2d;border-radius:6px">No chart data — market may be closed or symbol not found</div>', unsafe_allow_html=True)

    # Center tab strip
    ctabs = ["Overview", "Fundamentals", "Financials", "Sectors"]
    ct_cols = st.columns(len(ctabs))
    for i, t in enumerate(ctabs):
        tp = "primary" if st.session_state.ctab == t else "secondary"
        if ct_cols[i].button(t, key=f"ctab_{t}", type=tp):
            st.session_state.ctab = t; st.rerun()

    # ─── OVERVIEW ─────────────────────────────────────────────────────────────
    if st.session_state.ctab == "Overview":
        st.markdown('<div class="st2">// Key Metrics</div>', unsafe_allow_html=True)
        mcap  = info.get("marketCap")
        wh52  = info.get("fiftyTwoWeekHigh")
        wl52  = info.get("fiftyTwoWeekLow")
        pe_   = info.get("trailingPE")
        fpe   = info.get("forwardPE")
        eps   = info.get("trailingEps")
        dy    = info.get("dividendYield")
        vol   = info.get("volume") or info.get("regularMarketVolume")
        avol  = info.get("averageVolume") or info.get("averageDailyVolume3Month")
        beta  = info.get("beta")
        ptb   = info.get("priceToBook")

        metrics = [
            ("Mkt Cap",   fmt_inr(mcap),   ""),
            ("52W High",  safe(wh52),       "g" if wh52 and p and p >= wh52*0.95 else ""),
            ("52W Low",   safe(wl52),       "r" if wl52 and p and p <= wl52*1.05 else ""),
            ("P/E Ratio", safe(pe_,"",dec=2),""),
            ("Fwd P/E",   safe(fpe,"",dec=2),""),
            ("EPS (TTM)", safe(eps),        ""),
            ("Div Yield", safe(dy,fmt="pct"),"g" if dy and dy > 0 else ""),
            ("Volume",    safe(vol,fmt="vol"),""),
            ("Avg Vol",   safe(avol,fmt="vol"),""),
            ("Beta",      safe(beta,"",dec=2),""),
            ("P/Book",    safe(ptb,"",dec=2),""),
            ("Prev Close",safe(pc),         ""),
        ]
        mc4 = st.columns(4)
        for idx_, (lbl, val, vc) in enumerate(metrics):
            mvc = "mv-g" if vc == "g" else ("mv-r" if vc == "r" else "mv")
            with mc4[idx_ % 4]:
                st.markdown(f"""<div class="mc">
                  <div class="ml">{lbl}</div>
                  <div class="{mvc}">{val}</div>
                </div>""", unsafe_allow_html=True)

    # ─── FUNDAMENTALS ─────────────────────────────────────────────────────────
    elif st.session_state.ctab == "Fundamentals":
        roe  = info.get("returnOnEquity")
        roa  = info.get("returnOnAssets")
        gm   = info.get("grossMargins")
        om   = info.get("operatingMargins")
        pm   = info.get("profitMargins")
        d2e  = info.get("debtToEquity")
        cr   = info.get("currentRatio")
        fcf  = info.get("freeCashflow")
        rev  = info.get("totalRevenue")
        ebit = info.get("ebitda")
        ni   = info.get("netIncomeToCommon")
        eg   = info.get("earningsGrowth")
        rg   = info.get("revenueGrowth")
        bv   = info.get("bookValue")
        td   = info.get("totalDebt")
        tc   = info.get("totalCash")
        shr  = info.get("sharesOutstanding")
        fl   = info.get("floatShares")
        evr  = info.get("enterpriseToRevenue")
        eve  = info.get("enterpriseToEbitda")
        qeg  = info.get("earningsQuarterlyGrowth")
        tde  = info.get("trailingEps")

        fa, fb = st.columns(2)
        with fa:
            st.markdown('<div class="st2">// Profitability</div>', unsafe_allow_html=True)
            rows1 = [
                ("Revenue",          fmt_inr(rev)),
                ("EBITDA",           fmt_inr(ebit)),
                ("Net Income",       fmt_inr(ni)),
                ("Free Cash Flow",   fmt_inr(fcf)),
                ("Gross Margin",     safe(gm,  fmt="pct")),
                ("Operating Margin", safe(om,  fmt="pct")),
                ("Net Margin",       safe(pm,  fmt="pct")),
                ("ROE",              safe(roe, fmt="pct")),
                ("ROA",              safe(roa, fmt="pct")),
                ("EV/Revenue",       safe(evr, "", dec=2)),
                ("EV/EBITDA",        safe(eve, "", dec=2)),
                ("Rev Growth (YoY)", safe(rg,  fmt="pct")),
                ("Earn Growth (YoY)",safe(eg,  fmt="pct")),
                ("Earn Growth (QoQ)",safe(qeg, fmt="pct")),
            ]
            st.markdown('<table class="ft">', unsafe_allow_html=True)
            for lbl, val in rows1:
                st.markdown(f'<tr><td class="fl">{lbl}</td><td class="fv">{val}</td></tr>', unsafe_allow_html=True)
            st.markdown('</table>', unsafe_allow_html=True)

        with fb:
            st.markdown('<div class="st2">// Balance Sheet</div>', unsafe_allow_html=True)
            rows2 = [
                ("Total Debt",       fmt_inr(td)),
                ("Total Cash",       fmt_inr(tc)),
                ("Net Debt",         fmt_inr((td or 0) - (tc or 0)) if td and tc else "—"),
                ("Debt/Equity",      safe(d2e, "", dec=2)),
                ("Current Ratio",    safe(cr,  "", dec=2)),
                ("Book Value/Share", safe(bv,  dec=2)),
                ("Shares Out",       safe(shr, fmt="vol")),
                ("Float Shares",     safe(fl,  fmt="vol")),
                ("EPS (TTM)",        safe(tde, dec=2)),
            ]
            st.markdown('<table class="ft">', unsafe_allow_html=True)
            for lbl, val in rows2:
                st.markdown(f'<tr><td class="fl">{lbl}</td><td class="fv">{val}</td></tr>', unsafe_allow_html=True)
            st.markdown('</table>', unsafe_allow_html=True)

            st.markdown('<div class="st2" style="margin-top:12px">// Company</div>', unsafe_allow_html=True)
            info_rows = [
                ("Sector",   info.get("sector","—")),
                ("Industry", info.get("industry","—")),
                ("Exchange", info.get("exchange","—")),
                ("Country",  info.get("country","India")),
                ("Website",  f'<a href="{info.get("website","#")}" style="color:#3b82f6" target="_blank">{(info.get("website","—") or "—")[:30]}</a>'),
            ]
            st.markdown('<table class="ft">', unsafe_allow_html=True)
            for lbl, val in info_rows:
                st.markdown(f'<tr><td class="fl">{lbl}</td><td class="fv">{val}</td></tr>', unsafe_allow_html=True)
            st.markdown('</table>', unsafe_allow_html=True)

        # Business summary
        summary = info.get("longBusinessSummary","")
        if summary:
            st.markdown(f'<div style="font-size:0.7rem;color:#475569;line-height:1.65;margin-top:12px;padding:12px 14px;background:#0b0d16;border:1px solid #161c2d;border-radius:5px">{summary[:700]}…</div>', unsafe_allow_html=True)

    # ─── FINANCIALS ───────────────────────────────────────────────────────────
    elif st.session_state.ctab == "Financials":
        fin, bs, cf = get_financials(st.session_state.sel_sym)

        def render_fin_df(df_in, label):
            if df_in is None or df_in.empty:
                st.markdown(f'<div style="padding:10px;color:#1e3a5f;font-family:JetBrains Mono,monospace;font-size:0.65rem">{label}: data not available</div>', unsafe_allow_html=True)
                return
            st.markdown(f'<div class="st2">// {label}</div>', unsafe_allow_html=True)
            disp = df_in.head(10).copy()
            disp.index = [str(x)[:40] for x in disp.index]
            disp.columns = [str(c)[:12] for c in disp.columns]
            def fmt_cell(x):
                try:
                    f = float(x)
                    if abs(f) >= 1e7: return f"₹{f/1e7:.1f}Cr"
                    if abs(f) >= 1e5: return f"₹{f/1e5:.1f}L"
                    return f"₹{f:,.0f}"
                except: return "—"
            styled = disp.map(fmt_cell)
            st.dataframe(styled, use_container_width=True)

        render_fin_df(fin, "Income Statement (Annual)")
        render_fin_df(bs,  "Balance Sheet (Annual)")
        render_fin_df(cf,  "Cash Flow (Annual)")

    # ─── SECTORS ──────────────────────────────────────────────────────────────
    elif st.session_state.ctab == "Sectors":
        st.markdown('<div class="st2">// Sector Performance Today</div>', unsafe_allow_html=True)
        sc4 = st.columns(4)
        for i, s in enumerate(SECTOR_INDICES):
            q_s = get_quote(s["sym"])
            arr_s, col_s = ud(q_s["pct"])
            with sc4[i % 4]:
                st.markdown(f"""<div class="sectile">
                  <div class="secn">{s['name']}</div>
                  <div class="secp" style="color:{col_s}">{arr_s} {abs(q_s['pct']):.2f}%</div>
                </div>""", unsafe_allow_html=True)

        st.markdown('<div class="st2" style="margin-top:14px">// Sector 1M Normalised Return (%)</div>', unsafe_allow_html=True)
        sfig = go.Figure()
        pal  = ["#22c55e","#3b82f6","#f59e0b","#a855f7","#ef4444","#06b6d4","#f97316","#84cc16"]
        for si, s in enumerate(SECTOR_INDICES):
            sdf = get_hist(s["sym"], "1mo", "1d")
            if not sdf.empty and "Close" in sdf.columns and len(sdf) > 1:
                base = float(sdf["Close"].iloc[0])
                norm = (sdf["Close"].astype(float) / base - 1) * 100
                sfig.add_trace(go.Scatter(
                    x=sdf.index, y=norm.round(2), mode="lines",
                    name=s["name"], line=dict(color=pal[si], width=1.5)))
        sfig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0,r=4,t=4,b=0), height=240,
            hovermode="x unified",
            legend=dict(orientation="h", y=1.1, font=dict(family="JetBrains Mono",
                        size=10, color="#475569"), bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(showgrid=False, zeroline=False, color="#334155",
                       tickfont=dict(family="JetBrains Mono", size=10, color="#334155")),
            yaxis=dict(showgrid=True, gridcolor="#0f1220", zeroline=True,
                       zerolinecolor="#1c2238", side="right", ticksuffix="%",
                       tickfont=dict(family="JetBrains Mono", size=10, color="#334155")),
            hoverlabel=dict(bgcolor="#10131e", bordercolor="#1c2238",
                            font=dict(family="JetBrains Mono", size=11, color="#e2e8f0")),
        )
        st.plotly_chart(sfig, use_container_width=True, config={"displayModeBar": False})


# ══════════════ RIGHT ═════════════════════════════════════════════════════════
with R:
    RIGHT_TABS = ["Gainers", "Losers", "Indices", "Commodities", "MCX"]
    rtc = st.columns(len(RIGHT_TABS))
    for i, t in enumerate(RIGHT_TABS):
        tp = "primary" if st.session_state.right_tab == t else "secondary"
        if rtc[i].button(t, key=f"rt_{t}", type=tp):
            st.session_state.right_tab = t; st.rerun()

    tab = st.session_state.right_tab

    if tab in ("Gainers", "Losers"):
        rows = []
        for sym in NIFTY50_SYMS:
            q_r  = get_quote(sym)
            base = sym.replace(".NS","")
            rows.append({"sym": base, "full": sym,
                         "name": NSE_STOCKS.get(base, base),
                         "price": q_r["price"], "pct": q_r["pct"]})
        rows.sort(key=lambda x: x["pct"], reverse=(tab == "Gainers"))
        for r in rows[:18]:
            arr_r, col_r = ud(r["pct"])
            p_s = f"₹{r['price']:,.2f}" if r["price"] else "—"
            tp  = "primary" if r["full"] == st.session_state.sel_sym else "secondary"
            if st.button(f"{r['sym']}  {p_s}  {arr_r}{abs(r['pct']):.2f}%",
                         key=f"r_{tab}_{r['sym']}", type=tp, use_container_width=True):
                st.session_state.sel_sym  = r["full"]
                st.session_state.sel_name = r["name"]
                st.rerun()

    elif tab == "Indices":
        all_idx = [
            {"sym":"^NSEI",         "name":"NIFTY 50"},
            {"sym":"^BSESN",        "name":"SENSEX"},
            {"sym":"^NSMIDCP",      "name":"NIFTY Midcap"},
            {"sym":"^CNXSMALLCAP",  "name":"NIFTY Smallcap"},
            {"sym":"^CNXBANK",      "name":"Bank NIFTY"},
            {"sym":"^CNXIT",        "name":"NIFTY IT"},
            {"sym":"^CNXPHARMA",    "name":"NIFTY Pharma"},
            {"sym":"^CNXFMCG",      "name":"NIFTY FMCG"},
            {"sym":"^CNXAUTO",      "name":"NIFTY Auto"},
            {"sym":"^CNXREALTY",    "name":"NIFTY Realty"},
            {"sym":"^CNXMETAL",     "name":"NIFTY Metal"},
            {"sym":"^CNXENERGY",    "name":"NIFTY Energy"},
            {"sym":"^CNXINFRA",     "name":"NIFTY Infra"},
            {"sym":"^CNXPSUBANK",   "name":"NIFTY PSU Bank"},
            {"sym":"^CNXPRIVATEBANK","name":"NIFTY Pvt Bank"},
            {"sym":"^CNXMIDCAP",    "name":"NIFTY Midcap 100"},
        ]
        for ix in all_idx:
            q_i = get_quote(ix["sym"])
            arr_i, _ = ud(q_i["pct"])
            p_s = f"{q_i['price']:,.2f}" if q_i["price"] else "—"
            tp  = "primary" if ix["sym"] == st.session_state.sel_sym else "secondary"
            if st.button(f"{ix['name']}  {p_s}  {arr_i}{abs(q_i['pct']):.2f}%",
                         key=f"ri_{ix['sym']}", type=tp, use_container_width=True):
                st.session_state.sel_sym  = ix["sym"]
                st.session_state.sel_name = ix["name"]
                st.rerun()

    elif tab == "Commodities":
        for c in COMMODITIES:
            q_c = get_quote(c["sym"])
            arr_c, _ = ud(q_c["pct"])
            p_s = f"{q_c['price']:,.2f}" if q_c["price"] else "—"
            tp  = "primary" if c["sym"] == st.session_state.sel_sym else "secondary"
            if st.button(f"{c['name']}  {p_s}  {arr_c}{abs(q_c['pct']):.2f}%",
                         key=f"rc_{c['sym']}", type=tp, use_container_width=True):
                st.session_state.sel_sym  = c["sym"]
                st.session_state.sel_name = c["name"]
                st.rerun()

    elif tab == "MCX":
        for m in MCX_LIST:
            q_m = get_quote(m["sym"])
            arr_m, _ = ud(q_m["pct"])
            base_m   = m["sym"].replace(".NS","")
            p_s  = f"₹{q_m['price']:,.2f}" if q_m["price"] else "—"
            tp   = "primary" if m["sym"] == st.session_state.sel_sym else "secondary"
            if st.button(f"{base_m}  {p_s}  {arr_m}{abs(q_m['pct']):.2f}%",
                         key=f"rm_{m['sym']}", type=tp, use_container_width=True):
                st.session_state.sel_sym  = m["sym"]
                st.session_state.sel_name = m["name"]
                st.rerun()

    # Mini sparkline
    st.markdown("<hr style='border:none;border-top:1px solid #161c2d;margin:8px 0'>", unsafe_allow_html=True)
    mdf = get_hist(st.session_state.sel_sym, "1mo", "1d")
    if not mdf.empty and "Close" in mdf.columns:
        lc_m = "#22c55e" if pct >= 0 else "#ef4444"
        fa_m = "rgba(34,197,94,0.1)" if pct >= 0 else "rgba(239,68,68,0.1)"
        mfig = go.Figure(go.Scatter(
            x=mdf.index, y=mdf["Close"].astype(float),
            mode="lines", line=dict(color=lc_m, width=1.5),
            fill="tozeroy", fillcolor=fa_m,
        ))
        mfig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0,r=0,t=0,b=0), height=55, showlegend=False,
            xaxis=dict(visible=False), yaxis=dict(visible=False),
        )
        sym_lbl = st.session_state.sel_sym.replace(".NS","").replace(".BO","")
        st.markdown(f'<div style="font-family:JetBrains Mono,monospace;font-size:0.52rem;color:#1e3a5f;padding:3px 4px;text-transform:uppercase;letter-spacing:0.1em">{sym_lbl} · 1M trend</div>', unsafe_allow_html=True)
        st.plotly_chart(mfig, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<hr style='border:none;border-top:1px solid #161c2d;margin:6px 0'>", unsafe_allow_html=True)
    if st.button("⟳  Refresh Data", use_container_width=True):
        st.cache_data.clear(); st.rerun()
    st.markdown('<div style="font-family:JetBrains Mono,monospace;font-size:0.52rem;color:#1c2c42;text-align:center;padding:4px 0">Yahoo Finance · 2min cache · ~15min delay</div>', unsafe_allow_html=True)
