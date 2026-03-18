import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timezone, timedelta
import requests, json

st.set_page_config(page_title="Dalal Terminal", page_icon="◈",
                   layout="wide", initial_sidebar_state="collapsed")

# ── STOCK UNIVERSE ─────────────────────────────────────────────────────────────
NSE_STOCKS = {
    "RELIANCE":"Reliance Industries","TCS":"Tata Consultancy Services",
    "HDFCBANK":"HDFC Bank","INFY":"Infosys","ICICIBANK":"ICICI Bank",
    "HINDUNILVR":"Hindustan Unilever","ITC":"ITC Limited",
    "SBIN":"State Bank of India","BHARTIARTL":"Bharti Airtel",
    "KOTAKBANK":"Kotak Mahindra Bank","LT":"Larsen & Toubro",
    "AXISBANK":"Axis Bank","ASIANPAINT":"Asian Paints","MARUTI":"Maruti Suzuki",
    "TITAN":"Titan Company","WIPRO":"Wipro","BAJFINANCE":"Bajaj Finance",
    "NESTLEIND":"Nestle India","ULTRACEMCO":"UltraTech Cement",
    "TECHM":"Tech Mahindra","SUNPHARMA":"Sun Pharmaceutical",
    "HCLTECH":"HCL Technologies","POWERGRID":"Power Grid Corp",
    "NTPC":"NTPC Limited","TATAMOTORS":"Tata Motors","TATASTEEL":"Tata Steel",
    "HINDALCO":"Hindalco Industries","JSWSTEEL":"JSW Steel",
    "ONGC":"Oil & Natural Gas Corp","BPCL":"Bharat Petroleum",
    "IOC":"Indian Oil Corporation","COALINDIA":"Coal India",
    "GRASIM":"Grasim Industries","ADANIENT":"Adani Enterprises",
    "ADANIPORTS":"Adani Ports","ADANIGREEN":"Adani Green Energy",
    "AMBUJACEM":"Ambuja Cements","APOLLOHOSP":"Apollo Hospitals",
    "BAJAJFINSV":"Bajaj Finserv","BAJAJ-AUTO":"Bajaj Auto",
    "BANDHANBNK":"Bandhan Bank","BERGEPAINT":"Berger Paints",
    "BIOCON":"Biocon","BOSCHLTD":"Bosch","BRITANNIA":"Britannia Industries",
    "CANBK":"Canara Bank","CHOLAFIN":"Cholamandalam Finance","CIPLA":"Cipla",
    "COLPAL":"Colgate-Palmolive","DABUR":"Dabur India",
    "DIVISLAB":"Divi's Laboratories","DLF":"DLF",
    "DRREDDY":"Dr. Reddy's Laboratories","EICHERMOT":"Eicher Motors",
    "FEDERALBNK":"Federal Bank","GAIL":"GAIL India",
    "GODREJCP":"Godrej Consumer","GODREJPROP":"Godrej Properties",
    "HDFCAMC":"HDFC AMC","HDFCLIFE":"HDFC Life Insurance",
    "HEROMOTOCO":"Hero MotoCorp","HINDZINC":"Hindustan Zinc",
    "IDFCFIRSTB":"IDFC First Bank","INDHOTEL":"Indian Hotels",
    "INDIGO":"IndiGo","INDUSINDBK":"IndusInd Bank",
    "INDUSTOWER":"Indus Towers","IRCTC":"IRCTC","JSWENERGY":"JSW Energy",
    "JUBLFOOD":"Jubilant FoodWorks","LICI":"LIC India","LTIM":"LTIMindtree",
    "LUPIN":"Lupin","M&M":"Mahindra & Mahindra","MARICO":"Marico",
    "MPHASIS":"Mphasis","MRF":"MRF","MUTHOOTFIN":"Muthoot Finance",
    "NAUKRI":"Info Edge (Naukri)","NMDC":"NMDC","OBEROIRLTY":"Oberoi Realty",
    "OFSS":"Oracle Financial Services","PAGEIND":"Page Industries",
    "PERSISTENT":"Persistent Systems","PETRONET":"Petronet LNG",
    "PFC":"Power Finance Corp","PIDILITIND":"Pidilite Industries",
    "PNB":"Punjab National Bank","POLYCAB":"Polycab India",
    "RECLTD":"REC Limited","SAIL":"SAIL","SHREECEM":"Shree Cement",
    "SIEMENS":"Siemens India","SRF":"SRF Limited",
    "SRTRANSFIN":"Shriram Finance","TATACOMM":"Tata Communications",
    "TATACONSUM":"Tata Consumer Products","TATAELXSI":"Tata Elxsi",
    "TATAPOWER":"Tata Power","TORNTPHARM":"Torrent Pharmaceuticals",
    "TORNTPOWER":"Torrent Power","TRENT":"Trent","TVSMOTOR":"TVS Motor",
    "UBL":"United Breweries","UNIONBANK":"Union Bank of India","UPL":"UPL",
    "VEDL":"Vedanta","VOLTAS":"Voltas","YESBANK":"Yes Bank","ZOMATO":"Zomato",
    "PAYTM":"Paytm","NYKAA":"Nykaa","DELHIVERY":"Delhivery",
    "POLICYBZR":"PolicyBazaar","MANKIND":"Mankind Pharma","HAL":"HAL",
    "HAVELLS":"Havells India","LODHA":"Macrotech (Lodha)","MAXHEALTH":"Max Healthcare",
    "MCX":"MCX India","PHOENIXLTD":"Phoenix Mills","PRESTIGE":"Prestige Estates",
    "VBL":"Varun Beverages","PIIND":"PI Industries","BALKRISIND":"Balkrishna Industries",
    "DEEPAKNTR":"Deepak Nitrite","IRFC":"IRFC","LICHSGFIN":"LIC Housing Finance",
    "LTTS":"L&T Tech Services","NH":"Narayana Hrudayalaya",
    "NLCINDIA":"NLC India","OLECTRA":"Olectra Greentech",
    "PVR":"PVR INOX","RBLBANK":"RBL Bank","RITES":"RITES",
    "SCHAEFFLER":"Schaeffler India","SOBHA":"Sobha","STARHEALTH":"Star Health",
    "SUNDARMFIN":"Sundaram Finance","SUPREMEIND":"Supreme Industries",
    "TANLA":"Tanla Platforms","THERMAX":"Thermax","TIINDIA":"Tube Investments",
    "TRIDENT":"Trident","VINATIORGA":"Vinati Organics",
    "ZEEL":"Zee Entertainment","ZYDUSLIFE":"Zydus Lifesciences",
    "KPITTECH":"KPIT Technologies","KAYNES":"Kaynes Technology",
    "MAPMYINDIA":"MapmyIndia","CAMPUS":"Campus Activewear",
}
INDICES = [
    {"sym":"^NSEI","name":"NIFTY 50"},{"sym":"^BSESN","name":"SENSEX"},
    {"sym":"^NSMIDCP","name":"NIFTY MID"},{"sym":"^CNXIT","name":"NIFTY IT"},
    {"sym":"^CNXBANK","name":"BANK NIFTY"},
]
COMMODITIES = [
    {"sym":"GC=F","name":"Gold"},{"sym":"SI=F","name":"Silver"},
    {"sym":"CL=F","name":"Crude Oil"},{"sym":"NG=F","name":"Nat Gas"},
    {"sym":"USDINR=X","name":"USD/INR"},{"sym":"EURINR=X","name":"EUR/INR"},
    {"sym":"GBPINR=X","name":"GBP/INR"},
]
MCX_LIST = [
    {"sym":"TATASTEEL.NS","name":"Tata Steel"},{"sym":"HINDALCO.NS","name":"Hindalco"},
    {"sym":"JSWSTEEL.NS","name":"JSW Steel"},{"sym":"VEDL.NS","name":"Vedanta"},
    {"sym":"NMDC.NS","name":"NMDC"},{"sym":"SAIL.NS","name":"SAIL"},
    {"sym":"HINDZINC.NS","name":"Hindustan Zinc"},{"sym":"ONGC.NS","name":"ONGC"},
    {"sym":"BPCL.NS","name":"BPCL"},{"sym":"IOC.NS","name":"Indian Oil"},
    {"sym":"GAIL.NS","name":"GAIL"},{"sym":"MCX.NS","name":"MCX India"},
]
SECTORS = [
    {"sym":"^CNXIT","name":"IT"},{"sym":"^CNXBANK","name":"Banking"},
    {"sym":"^CNXPHARMA","name":"Pharma"},{"sym":"^CNXFMCG","name":"FMCG"},
    {"sym":"^CNXAUTO","name":"Auto"},{"sym":"^CNXREALTY","name":"Realty"},
    {"sym":"^CNXMETAL","name":"Metal"},{"sym":"^CNXENERGY","name":"Energy"},
]
ALL_IDX = [
    {"sym":"^NSEI","name":"NIFTY 50"},{"sym":"^BSESN","name":"SENSEX"},
    {"sym":"^NSMIDCP","name":"NIFTY Midcap"},{"sym":"^CNXSMALLCAP","name":"NIFTY Smallcap"},
    {"sym":"^CNXBANK","name":"Bank NIFTY"},{"sym":"^CNXIT","name":"NIFTY IT"},
    {"sym":"^CNXPHARMA","name":"NIFTY Pharma"},{"sym":"^CNXFMCG","name":"NIFTY FMCG"},
    {"sym":"^CNXAUTO","name":"NIFTY Auto"},{"sym":"^CNXREALTY","name":"NIFTY Realty"},
    {"sym":"^CNXMETAL","name":"NIFTY Metal"},{"sym":"^CNXENERGY","name":"NIFTY Energy"},
    {"sym":"^CNXINFRA","name":"NIFTY Infra"},{"sym":"^CNXPSUBANK","name":"NIFTY PSU Bank"},
    {"sym":"^CNXPRIVATEBANK","name":"NIFTY Pvt Bank"},
]
NIFTY50 = [k+".NS" for k in [
    "RELIANCE","TCS","HDFCBANK","INFY","ICICIBANK","HINDUNILVR","ITC","SBIN",
    "BHARTIARTL","KOTAKBANK","LT","AXISBANK","ASIANPAINT","MARUTI","TITAN",
    "WIPRO","BAJFINANCE","NESTLEIND","ULTRACEMCO","TECHM","SUNPHARMA","HCLTECH",
    "POWERGRID","NTPC","TATAMOTORS","HINDALCO","JSWSTEEL","ONGC","BPCL",
    "COALINDIA","GRASIM","ADANIENT","ADANIPORTS","TATASTEEL","BAJAJFINSV",
    "BAJAJ-AUTO","DIVISLAB","DRREDDY","EICHERMOT","HEROMOTOCO","INDUSINDBK",
    "M&M","TATACONSUM","TATAPOWER","TRENT","UPL","VEDL","BRITANNIA","CIPLA","LUPIN",
]]
PERIODS = {
    "1D":("1d","5m"),"1W":("5d","15m"),"1M":("1mo","1h"),
    "3M":("3mo","1d"),"6M":("6mo","1d"),"1Y":("1y","1d"),"3Y":("3y","1wk"),
}
IST = timezone(timedelta(hours=5, minutes=30))

# ── SESSION STATE ──────────────────────────────────────────────────────────────
def ss(k,v):
    if k not in st.session_state: st.session_state[k]=v

ss("watchlist",[
    {"sym":"RELIANCE.NS","name":"Reliance Industries"},
    {"sym":"TCS.NS","name":"Tata Consultancy Services"},
    {"sym":"HDFCBANK.NS","name":"HDFC Bank"},
    {"sym":"INFY.NS","name":"Infosys"},
    {"sym":"ICICIBANK.NS","name":"ICICI Bank"},
    {"sym":"SBIN.NS","name":"State Bank of India"},
    {"sym":"TATAMOTORS.NS","name":"Tata Motors"},
    {"sym":"WIPRO.NS","name":"Wipro"},
])
ss("sel","RELIANCE.NS"); ss("sel_name","Reliance Industries")
ss("period","1M"); ss("ctype","Candle"); ss("rtab","Gainers")
ss("ctab","Overview"); ss("nkey","")

# ── DATA ──────────────────────────────────────────────────────────────────────
def to_sym(raw):
    r=raw.strip().upper()
    if any(r.endswith(s) for s in [".NS",".BO","=F","=X"]) or r.startswith("^"): return r
    return r+".NS"

@st.cache_data(ttl=120,show_spinner=False)
def qget(sym):
    try:
        fi=yf.Ticker(sym).fast_info
        p=round(float(fi.last_price or 0),2)
        pc=round(float(fi.previous_close or 0),2)
        ch=round(p-pc,2); pct=round((ch/pc*100) if pc else 0,2)
        return {"p":p,"pc":pc,"ch":ch,"pct":pct,
                "hi":round(float(fi.day_high or 0),2),
                "lo":round(float(fi.day_low  or 0),2)}
    except: return {"p":0,"pc":0,"ch":0,"pct":0,"hi":0,"lo":0}

@st.cache_data(ttl=300,show_spinner=False)
def iget(sym):
    try: return yf.Ticker(sym).info or {}
    except: return {}

@st.cache_data(ttl=180,show_spinner=False)
def hget(sym,period,interval):
    try:
        df=yf.download(sym,period=period,interval=interval,progress=False,auto_adjust=True)
        if isinstance(df.columns,pd.MultiIndex): df.columns=df.columns.get_level_values(0)
        return df.dropna(how="all")
    except: return pd.DataFrame()

@st.cache_data(ttl=300,show_spinner=False)
def fget(sym):
    try:
        t=yf.Ticker(sym)
        return t.financials,t.balance_sheet,t.cashflow
    except: return None,None,None

@st.cache_data(ttl=300,show_spinner=False)
def news_get(key,q):
    if not key: return []
    try:
        r=requests.get("https://newsapi.org/v2/everything",
            params={"q":q,"apiKey":key,"sortBy":"publishedAt","pageSize":15,"language":"en"},timeout=8)
        d=r.json(); return d.get("articles",[]) if d.get("status")=="ok" else []
    except: return []

def tago(s):
    try:
        d=int((datetime.now(timezone.utc)-datetime.strptime(s,"%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)).total_seconds())
        if d<3600: return f"{d//60}m ago"
        if d<86400: return f"{d//3600}h ago"
        return f"{d//86400}d ago"
    except: return ""

def finr(v):
    try:
        v=float(v)
        if v==0: return "—"
        if v>=1e12: return f"₹{v/1e12:.2f}T"
        if v>=1e9:  return f"₹{v/1e9:.2f}B"
        if v>=1e7:  return f"₹{v/1e7:.1f}Cr"
        if v>=1e5:  return f"₹{v/1e5:.1f}L"
        return f"₹{v:,.2f}"
    except: return "—"

def sv(v,pre="₹",dec=2,fmt=None):
    if v is None: return "—"
    try:
        f=float(v)
        if f==0: return "—"
        if fmt=="pct": return f"{f*100:.{dec}f}%"
        if fmt=="vol":
            if f>=1e7: return f"{f/1e7:.2f}Cr"
            if f>=1e5: return f"{f/1e5:.1f}L"
            return f"{int(f):,}"
        return f"{pre}{f:,.{dec}f}"
    except: return "—"

def ud(pct): return ("▲","#16a34a") if pct>=0 else ("▼","#dc2626")
def sc(pct): return "pos" if pct>=0 else "neg"

def calc_technicals(df):
    """Compute technical indicators from OHLCV dataframe."""
    if df.empty or "Close" not in df.columns:
        return {}
    c = df["Close"].astype(float)
    t = {}
    # Moving averages
    if len(c) >= 20:  t["MA20"] = round(float(c.rolling(20).mean().iloc[-1]), 2)
    if len(c) >= 50:  t["MA50"] = round(float(c.rolling(50).mean().iloc[-1]), 2)
    if len(c) >= 200: t["MA200"]= round(float(c.rolling(200).mean().iloc[-1]), 2)
    # RSI
    if len(c) >= 15:
        delta = c.diff()
        gain  = delta.clip(lower=0).rolling(14).mean()
        loss  = (-delta.clip(upper=0)).rolling(14).mean()
        rs    = gain / loss.replace(0, float("nan"))
        rsi   = 100 - (100 / (1 + rs))
        t["RSI14"] = round(float(rsi.iloc[-1]), 1)
    # MACD
    if len(c) >= 26:
        ema12 = c.ewm(span=12, adjust=False).mean()
        ema26 = c.ewm(span=26, adjust=False).mean()
        macd  = ema12 - ema26
        signal= macd.ewm(span=9, adjust=False).mean()
        t["MACD"]       = round(float(macd.iloc[-1]), 2)
        t["MACD_Signal"]= round(float(signal.iloc[-1]), 2)
        t["MACD_Hist"]  = round(float((macd - signal).iloc[-1]), 2)
    # Bollinger Bands
    if len(c) >= 20:
        ma = c.rolling(20).mean()
        sd = c.rolling(20).std()
        t["BB_Upper"] = round(float((ma + 2*sd).iloc[-1]), 2)
        t["BB_Lower"] = round(float((ma - 2*sd).iloc[-1]), 2)
        t["BB_Mid"]   = round(float(ma.iloc[-1]), 2)
    # Volatility (annualised)
    if len(c) >= 20:
        daily_ret = c.pct_change().dropna()
        t["Volatility_Ann%"] = round(float(daily_ret.std() * (252**0.5) * 100), 1)
    # Price vs MAs
    cur = float(c.iloc[-1])
    t["Current_Price"] = cur
    t["1M_Return%"]  = round((cur / float(c.iloc[-min(22,len(c))])  - 1)*100, 2)
    t["3M_Return%"]  = round((cur / float(c.iloc[-min(66,len(c))])  - 1)*100, 2)
    t["6M_Return%"]  = round((cur / float(c.iloc[-min(130,len(c))]) - 1)*100, 2)
    # Average volume ratio
    if "Volume" in df.columns:
        v = df["Volume"].astype(float)
        if len(v) >= 10:
            t["Vol_Ratio_10d"] = round(float(v.iloc[-5:].mean() / v.iloc[-20:].mean()), 2)
    return t

def call_claude(prompt: str) -> str:
    """Call Anthropic API and return streamed text."""
    try:
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={"Content-Type": "application/json"},
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 1000,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=60,
        )
        data = resp.json()
        return "".join(b.get("text","") for b in data.get("content",[]) if b.get("type")=="text")
    except Exception as e:
        return f"⚠ Could not reach AI: {e}"

def do_search(q):
    q=q.strip().upper()
    if len(q)<2: return []
    return [{"sym":k,"name":v} for k,v in NSE_STOCKS.items()
            if q in k or q in v.upper()][:7]

# ── IST TIME ──────────────────────────────────────────────────────────────────
now_ist = datetime.now(IST)
now_str = now_ist.strftime("%d %b %Y  %H:%M IST")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap');

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}

html,body,[class*="css"]{
  font-family:'Inter',sans-serif;
  background:#f0f2f5 !important;
  color:#1e293b;
}

/* ── HIDE STREAMLIT CHROME ── */
.main .block-container{
  padding: 0 !important;
  max-width: 100% !important;
}
section[data-testid="stSidebar"]{ display:none !important }
#MainMenu,footer,header,[data-testid="stToolbar"],.stDeployButton{ display:none !important }
::-webkit-scrollbar{ width:4px; background:transparent }
::-webkit-scrollbar-thumb{ background:#cbd5e1; border-radius:4px }

/* ── TOPBAR ── */
.topbar{
  display:flex; align-items:center; gap:8px;
  padding:0 20px; height:52px;
  background:#fff;
  border-bottom:1px solid #e2e8f0;
  position:sticky; top:0; z-index:200;
  box-shadow:0 1px 4px rgba(0,0,0,0.06);
  overflow-x:auto;
}
.t-logo{
  font-family:'JetBrains Mono',monospace;
  font-size:0.8rem; font-weight:600; color:#0f172a;
  letter-spacing:0.14em; white-space:nowrap;
  display:flex; align-items:center; gap:5px; margin-right:8px;
}
.t-dot{ color:#f97316 }
.ic{
  display:flex; flex-direction:column; justify-content:center;
  padding:4px 12px; border-radius:6px;
  background:#f8fafc; border:1px solid #e2e8f0;
  min-width:90px; white-space:nowrap;
}
.ic-n{ font-size:0.52rem; color:#94a3b8; letter-spacing:0.08em; text-transform:uppercase; font-family:'JetBrains Mono',monospace }
.ic-v{ font-family:'JetBrains Mono',monospace; font-size:0.78rem; font-weight:600; color:#0f172a; line-height:1.3 }
.ic-c{ font-family:'JetBrains Mono',monospace; font-size:0.6rem; font-weight:500 }
.ic-c.pos{ color:#16a34a } .ic-c.neg{ color:#dc2626 }
.t-r{ margin-left:auto; display:flex; align-items:center; gap:10px; flex-shrink:0 }
.t-time{ font-family:'JetBrains Mono',monospace; font-size:0.6rem; color:#94a3b8; white-space:nowrap }
.t-live{ font-size:0.6rem; color:#16a34a; background:#f0fdf4; border:1px solid #bbf7d0; padding:2px 8px; border-radius:20px; font-weight:500; font-family:'JetBrains Mono',monospace; white-space:nowrap }

/* ── THREE-PANEL LAYOUT ──
   We target Streamlit's column wrappers directly by nth-child.
   Column 1 = Left panel (white, border-right)
   Column 2 = Center panel (light grey bg)
   Column 3 = Right panel (white, border-left)
*/

/* Remove default column padding */
[data-testid="column"] { padding: 0 !important; }

/* Left column */
[data-testid="column"]:nth-of-type(1) > div:first-child {
  background: #ffffff;
  border-right: 1px solid #e2e8f0;
  height: calc(100vh - 52px);
  overflow-y: auto;
  overflow-x: hidden;
}

/* Center column */
[data-testid="column"]:nth-of-type(2) > div:first-child {
  background: #f0f2f5;
  height: calc(100vh - 52px);
  overflow-y: auto;
  padding: 14px 16px;
}

/* Right column */
[data-testid="column"]:nth-of-type(3) > div:first-child {
  background: #ffffff;
  border-left: 1px solid #e2e8f0;
  height: calc(100vh - 52px);
  overflow-y: auto;
  overflow-x: hidden;
}

/* ── SECTION HEADER ── */
.sh{
  font-size:0.58rem; font-weight:600; color:#94a3b8;
  letter-spacing:0.12em; text-transform:uppercase;
  padding:10px 14px 8px;
  border-bottom:1px solid #f1f5f9;
  background:#fff;
}

/* ── SEARCH RESULTS ── */
.sr-drop{
  background:#fff; border:1px solid #e2e8f0;
  border-radius:6px; margin:0 10px 4px;
  box-shadow:0 4px 12px rgba(0,0,0,0.08); overflow:hidden;
}
.sr-row{
  padding:7px 10px; border-bottom:1px solid #f8fafc;
  transition:background 0.1s; cursor:pointer;
}
.sr-row:last-child{ border-bottom:none }
.sr-row:hover{ background:#fef9f5 }
.sr-sym{ font-family:'JetBrains Mono',monospace; font-size:0.72rem; font-weight:600; color:#f97316 }
.sr-nm{ font-size:0.62rem; color:#64748b; margin-top:1px }

/* ── WATCHLIST ROW ── */
.wl-outer{
  display:flex; align-items:stretch;
  border-bottom:1px solid #f8fafc;
  transition:background 0.1s;
}
.wl-outer:hover{ background:#fef9f5 }
.wl-outer.wl-sel{ background:#fff7ed; border-left:3px solid #f97316 }
.wl-info{ display:flex; flex-direction:column; justify-content:center;
  padding:7px 4px 7px 12px; flex:1; min-width:0; cursor:pointer }
.wl-sym{ font-family:'JetBrains Mono',monospace; font-size:0.7rem; font-weight:600; color:#1e293b }
.wl-meta{ display:flex; align-items:center; gap:6px; margin-top:2px }
.wl-price{ font-family:'JetBrains Mono',monospace; font-size:0.68rem; color:#374151 }
.wl-pct{ font-size:0.62rem; font-weight:500; padding:1px 5px; border-radius:3px }
.wl-pct.pos{ color:#16a34a; background:#f0fdf4 }
.wl-pct.neg{ color:#dc2626; background:#fef2f2 }

/* ── NEWS ── */
.ni{ padding:8px 14px; border-bottom:1px solid #f8fafc; cursor:pointer; transition:background 0.1s }
.ni:hover{ background:#f8fafc }
.ni-s{ font-size:0.56rem; font-weight:600; color:#f97316; text-transform:uppercase; letter-spacing:0.06em }
.ni-t{ font-size:0.68rem; color:#334155; line-height:1.4; margin-top:2px }
.ni-d{ font-size:0.56rem; color:#94a3b8; margin-top:3px; font-family:'JetBrains Mono',monospace }

/* ── STOCK BANNER ── */
.banner{
  background:#fff; border-radius:10px; padding:14px 18px;
  border:1px solid #e2e8f0; margin-bottom:12px;
  box-shadow:0 1px 4px rgba(0,0,0,0.05);
}
.bn-name{ font-size:1rem; font-weight:600; color:#0f172a }
.bn-sub{ font-size:0.6rem; color:#94a3b8; margin-top:2px; font-family:'JetBrains Mono',monospace }
.bn-price{ font-family:'JetBrains Mono',monospace; font-size:1.85rem; font-weight:600; color:#0f172a; line-height:1; text-align:right }
.bn-chg{ font-family:'JetBrains Mono',monospace; font-size:0.78rem; font-weight:500; text-align:right; margin-top:4px }
.orow{ display:flex; gap:6px; flex-wrap:wrap; margin-top:10px }
.otag{ background:#f8fafc; border:1px solid #e2e8f0; border-radius:5px; padding:3px 10px; font-family:'JetBrains Mono',monospace; font-size:0.62rem }
.ol{ color:#94a3b8; margin-right:2px }
.ov{ color:#1e293b; font-weight:600 }
.ov-g{ color:#16a34a; font-weight:600 }
.ov-r{ color:#dc2626; font-weight:600 }

/* ── CHART AREA ── */
.chart-wrap{
  background:#fff; border:1px solid #e2e8f0;
  border-radius:10px; padding:10px 10px 4px;
  margin-bottom:12px;
  box-shadow:0 1px 4px rgba(0,0,0,0.05);
}

/* ── METRIC CARDS ── */
.mc{ background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:9px 11px; box-shadow:0 1px 3px rgba(0,0,0,0.04) }
.mc-l{ font-size:0.55rem; font-weight:500; color:#94a3b8; text-transform:uppercase; letter-spacing:0.08em }
.mc-v{ font-family:'JetBrains Mono',monospace; font-size:0.82rem; font-weight:600; color:#1e293b; margin-top:4px }
.mc-v.pos{ color:#16a34a } .mc-v.neg{ color:#dc2626 }

/* ── FUND TABLE ── */
.ft{ width:100%; border-collapse:collapse }
.ft td{ padding:6px 8px; border-bottom:1px solid #f8fafc; font-size:0.7rem }
.ft tr:hover td{ background:#fef9f5 }
.fl{ color:#64748b; font-size:0.65rem }
.fv{ color:#1e293b; text-align:right; font-family:'JetBrains Mono',monospace; font-size:0.7rem; font-weight:500 }

/* ── SECTOR TILE ── */
.sec-t{ background:#fff; border:1px solid #e2e8f0; border-radius:7px; padding:9px; text-align:center; box-shadow:0 1px 3px rgba(0,0,0,0.04) }
.sec-n{ font-size:0.57rem; font-weight:500; color:#94a3b8; text-transform:uppercase; letter-spacing:0.06em }
.sec-p{ font-family:'JetBrains Mono',monospace; font-size:0.85rem; font-weight:600; margin-top:4px }
.sec-p.pos{ color:#16a34a } .sec-p.neg{ color:#dc2626 }

/* ── RIGHT PANEL ROWS ── */
.rr{ display:flex; align-items:center; justify-content:space-between; padding:8px 14px; border-bottom:1px solid #f8fafc; cursor:pointer; transition:background 0.1s }
.rr:hover{ background:#fef9f5 }
.rr.rr-sel{ background:#fff7ed; border-left:3px solid #f97316 }
.rr-sym{ font-family:'JetBrains Mono',monospace; font-size:0.7rem; font-weight:600; color:#1e293b }
.rr-nm{ font-size:0.58rem; color:#94a3b8; margin-top:1px }
.rr-p{ font-family:'JetBrains Mono',monospace; font-size:0.7rem; font-weight:500; color:#374151; text-align:right }
.rr-c{ font-family:'JetBrains Mono',monospace; font-size:0.62rem; font-weight:500; text-align:right; margin-top:1px }
.rr-c.pos{ color:#16a34a } .rr-c.neg{ color:#dc2626 }

/* ── SECTION TITLE ── */
.sct{ font-size:0.6rem; font-weight:600; color:#94a3b8; letter-spacing:0.1em; text-transform:uppercase; padding:10px 0 8px; border-bottom:1px solid #f1f5f9; margin-bottom:12px }

/* ── AI ANALYSIS CARDS ── */
.ai-card{
  background:#fff; border:1px solid #e2e8f0; border-radius:10px;
  padding:16px 18px; margin-bottom:12px;
  box-shadow:0 1px 4px rgba(0,0,0,0.05);
}
.ai-card-header{
  display:flex; align-items:center; gap:8px; margin-bottom:12px;
  padding-bottom:10px; border-bottom:1px solid #f1f5f9;
}
.ai-badge{
  font-size:0.58rem; font-weight:600; letter-spacing:0.1em;
  text-transform:uppercase; padding:3px 9px; border-radius:20px;
}
.ai-badge-full{ background:#fff7ed; color:#f97316; border:1px solid #fed7aa }
.ai-badge-news{ background:#eff6ff; color:#2563eb; border:1px solid #bfdbfe }
.ai-badge-tech{ background:#f0fdf4; color:#16a34a; border:1px solid #bbf7d0 }
.ai-badge-fund{ background:#fdf4ff; color:#9333ea; border:1px solid #e9d5ff }
.ai-badge-fin{  background:#fff1f2; color:#e11d48; border:1px solid #fecdd3 }
.ai-card-title{ font-size:0.82rem; font-weight:600; color:#1e293b }
.ai-body{
  font-size:0.76rem; color:#374151; line-height:1.75;
  white-space:pre-wrap;
}
.ai-body strong{ font-weight:600; color:#1e293b }
.ai-spinner{
  display:flex; align-items:center; gap:8px;
  font-size:0.72rem; color:#94a3b8; padding:8px 0;
  font-family:'JetBrains Mono',monospace;
}
.ai-generate-btn{
  display:inline-flex; align-items:center; gap:6px;
  font-size:0.72rem; font-weight:500;
  background:#f97316; color:#fff;
  border:none; border-radius:6px; padding:7px 16px;
  cursor:pointer; transition:background 0.15s;
  font-family:'Inter',sans-serif;
}
.ai-generate-btn:hover{ background:#ea6c0a }
.ai-disclaimer{
  font-size:0.58rem; color:#94a3b8; margin-top:10px;
  padding-top:8px; border-top:1px solid #f1f5f9;
  font-style:italic;
}

/* ── STREAMLIT BUTTON OVERRIDES ── */
.stButton > button {
  font-family: 'Inter', sans-serif !important;
  font-size: 0.68rem !important;
  font-weight: 500 !important;
  border-radius: 6px !important;
  padding: 4px 10px !important;
  width: 100% !important;
  background: transparent !important;
  color: #94a3b8 !important;
  border: 1px solid #f1f5f9 !important;
  transition: all 0.12s !important;
  white-space: nowrap !important;
  margin-top: -2px !important;
  margin-bottom: 2px !important;
}
.stButton > button:hover {
  background: #fef9f5 !important;
  color: #f97316 !important;
  border-color: #fed7aa !important;
}
.stButton > button[kind="primary"] {
  background: #f97316 !important;
  color: #ffffff !important;
  border-color: #f97316 !important;
  font-weight: 600 !important;
}

/* ── TEXT INPUT OVERRIDES ── */
.stTextInput > div > div > input {
  background: #f8fafc !important;
  border: 1px solid #e2e8f0 !important;
  color: #1e293b !important;
  border-radius: 6px !important;
  font-size: 0.72rem !important;
  padding: 7px 10px !important;
  font-family: 'Inter', sans-serif !important;
}
.stTextInput > div > div > input:focus {
  border-color: #f97316 !important;
  box-shadow: 0 0 0 3px #fed7aa33 !important;
  background: #fff !important;
}
.stTextInput > div > div > input::placeholder { color: #94a3b8 !important }
.stTextInput label, [data-testid="stWidgetLabel"] {
  font-size: 0.56rem !important; font-weight: 600 !important;
  color: #94a3b8 !important; text-transform: uppercase !important;
  letter-spacing: 0.1em !important;
}

/* ── EXPANDER ── */
.streamlit-expanderHeader {
  background: #f8fafc !important;
  border: 1px solid #e2e8f0 !important;
  border-radius: 6px !important;
  font-size: 0.68rem !important;
  color: #64748b !important;
  padding: 6px 12px !important;
}
details[open] .streamlit-expanderHeader {
  border-radius: 6px 6px 0 0 !important;
}

/* ── DATAFRAME ── */
.stDataFrame { border-radius: 8px !important; border: 1px solid #e2e8f0 !important; overflow: hidden !important }
[data-testid="stPlotlyChart"] { border-radius: 8px; overflow: hidden }
</style>
""", unsafe_allow_html=True)

# ── TOPBAR ────────────────────────────────────────────────────────────────────
idx_q = {i["sym"]: qget(i["sym"]) for i in INDICES}
chips = ""
for i in INDICES:
    q = idx_q[i["sym"]]
    arr, _ = ud(q["pct"]); cls = sc(q["pct"])
    chips += f"""<div class="ic">
      <span class="ic-n">{i['name']}</span>
      <span class="ic-v">{q['p']:,.2f}</span>
      <span class="ic-c {cls}">{arr} {abs(q['pct']):.2f}%</span>
    </div>"""

st.markdown(f"""<div class="topbar">
  <span class="t-logo"><span class="t-dot">◈</span> DALAL</span>
  {chips}
  <div class="t-r">
    <span class="t-time">{now_str}</span>
    <span class="t-live">● LIVE</span>
  </div>
</div>""", unsafe_allow_html=True)

# ── COLUMNS ───────────────────────────────────────────────────────────────────
L, C, R = st.columns([2.1, 6.5, 2.4])

# ══════════════════════════════════ LEFT ══════════════════════════════════════
with L:
    # ── Search ──
    st.markdown('<div class="sh">Search &amp; Add</div>', unsafe_allow_html=True)
    raw_q = st.text_input("", placeholder="Search name or ticker (e.g. SBIN)…",
                          key="sq", label_visibility="collapsed")
    hits  = do_search(raw_q) if raw_q else []
    if hits:
        st.markdown('<div class="sr-drop">', unsafe_allow_html=True)
        for h in hits:
            ca, cb = st.columns([5, 1])
            with ca:
                st.markdown(f"""<div class="sr-row">
                  <div class="sr-sym">{h['sym']}</div>
                  <div class="sr-nm">{h['name']}</div>
                </div>""", unsafe_allow_html=True)
            with cb:
                if st.button("＋", key=f"a_{h['sym']}"):
                    e = {"sym": h["sym"]+".NS", "name": h["name"]}
                    if e not in st.session_state.watchlist:
                        st.session_state.watchlist.append(e)
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("Add by full ticker (e.g. SBIN.NS)"):
        mt = st.text_input("", placeholder="e.g. SBIN or SBIN.NS", key="mt",
                           label_visibility="collapsed")
        if st.button("Add to Watchlist", key="btn_mt"):
            if mt.strip():
                sym  = to_sym(mt)
                base = mt.strip().upper().replace(".NS","").replace(".BO","")
                nm   = NSE_STOCKS.get(base, base)
                e    = {"sym": sym, "name": nm}
                if e not in st.session_state.watchlist:
                    st.session_state.watchlist.append(e)
                st.rerun()

    # ── Watchlist ──
    st.markdown('<div class="sh">Watchlist</div>', unsafe_allow_html=True)
    to_del = None
    for i, w in enumerate(st.session_state.watchlist):
        q    = qget(w["sym"])
        base = w["sym"].replace(".NS","").replace(".BO","")
        arr, _ = ud(q["pct"]); cls = sc(q["pct"])
        ps   = f"₹{q['p']:,.2f}" if q["p"] else "—"
        pcs  = f"{arr}{abs(q['pct']):.2f}%"
        is_s = w["sym"] == st.session_state.sel
        sel_cls = "wl-outer wl-sel" if is_s else "wl-outer"

        st.markdown(f"""<div class="{sel_cls}">
          <div class="wl-info">
            <div class="wl-sym">{base}</div>
            <div class="wl-meta">
              <span class="wl-price">{ps}</span>
              <span class="wl-pct {cls}">{pcs}</span>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

        # invisible buttons for click and delete
        bc, bd = st.columns([5, 1])
        with bc:
            tp = "primary" if is_s else "secondary"
            if st.button(base, key=f"ws_{i}", type=tp):
                st.session_state.sel      = w["sym"]
                st.session_state.sel_name = w["name"]
                st.rerun()
        with bd:
            if st.button("✕", key=f"wd_{i}"):
                to_del = i

    if to_del is not None:
        st.session_state.watchlist.pop(to_del)
        syms = [w["sym"] for w in st.session_state.watchlist]
        if st.session_state.sel not in syms and syms:
            st.session_state.sel      = st.session_state.watchlist[0]["sym"]
            st.session_state.sel_name = st.session_state.watchlist[0]["name"]
        st.rerun()

    # ── News ──
    st.markdown('<div class="sh" style="margin-top:4px">News</div>', unsafe_allow_html=True)
    nk = st.text_input("", type="password", placeholder="NewsAPI key (newsapi.org)…",
                       key="nk_inp", label_visibility="collapsed")
    if nk: st.session_state.nkey = nk

    arts = news_get(st.session_state.nkey, f"India NSE BSE {st.session_state.sel_name}")
    if arts:
        for a in arts[:12]:
            src = (a.get("source",{}).get("name",""))[:22]
            ttl = (a.get("title",""))[:75]
            url = a.get("url","#")
            st.markdown(f"""<div class="ni" onclick="window.open('{url}','_blank')">
              <div class="ni-s">{src}</div>
              <div class="ni-t">{ttl}</div>
              <div class="ni-d">{tago(a.get('publishedAt',''))}</div>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div style="padding:12px 14px;font-size:0.65rem;color:#94a3b8">Enter NewsAPI key above for live news.</div>', unsafe_allow_html=True)


# ══════════════════════════════════ CENTER ════════════════════════════════════
with C:
    q    = qget(st.session_state.sel)
    info = iget(st.session_state.sel)
    arr, col = ud(q["pct"])
    p   = q["p"]; ch = q["ch"]; pct = q["pct"]
    hi  = q["hi"] or info.get("dayHigh") or 0
    lo  = q["lo"] or info.get("dayLow")  or 0
    op_ = info.get("open") or info.get("regularMarketOpen") or 0
    pc  = q["pc"] or info.get("previousClose") or 0

    # ── Banner ──
    st.markdown(f"""<div class="banner">
      <div style="display:flex;justify-content:space-between;align-items:flex-start">
        <div>
          <div class="bn-name">{st.session_state.sel_name}</div>
          <div class="bn-sub">{st.session_state.sel} · NSE/BSE</div>
          <div class="orow">
            <div class="otag"><span class="ol">O</span><span class="ov">{'₹'+f'{op_:,.2f}' if op_ else '—'}</span></div>
            <div class="otag"><span class="ol">H</span><span class="ov-g">{'₹'+f'{hi:,.2f}' if hi else '—'}</span></div>
            <div class="otag"><span class="ol">L</span><span class="ov-r">{'₹'+f'{lo:,.2f}' if lo else '—'}</span></div>
            <div class="otag"><span class="ol">PC</span><span class="ov">{'₹'+f'{pc:,.2f}' if pc else '—'}</span></div>
          </div>
        </div>
        <div>
          <div class="bn-price">{'₹'+f'{p:,.2f}' if p else '—'}</div>
          <div class="bn-chg" style="color:{col}">{arr} ₹{abs(ch):,.2f} &nbsp;({abs(pct):.2f}%)</div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    # ── Period + chart type ──
    btns = list(PERIODS.keys()) + ["Line","Candle","Area"]
    pcols = st.columns(len(btns))
    for i, lbl in enumerate(PERIODS.keys()):
        tp = "primary" if st.session_state.period == lbl else "secondary"
        if pcols[i].button(lbl, key=f"pb_{lbl}", type=tp):
            st.session_state.period = lbl; st.rerun()
    for j, ct in enumerate(["Line","Candle","Area"]):
        tp = "primary" if st.session_state.ctype == ct else "secondary"
        if pcols[len(PERIODS)+j].button(ct, key=f"cb_{ct}", type=tp):
            st.session_state.ctype = ct; st.rerun()

    # ── Chart ──
    pr, iv = PERIODS[st.session_state.period]
    df     = hget(st.session_state.sel, pr, iv)
    is_pos = pct >= 0
    GRN, RED = "#16a34a", "#dc2626"
    lc = GRN if is_pos else RED
    fa = "rgba(22,163,74,0.07)" if is_pos else "rgba(220,38,38,0.07)"

    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    if not df.empty and "Close" in df.columns:
        has_ohlc = all(c in df.columns for c in ["Open","High","Low","Close"])
        has_vol  = "Volume" in df.columns

        fig = make_subplots(
            rows=2, cols=1, shared_xaxes=True,
            row_heights=[0.74, 0.26], vertical_spacing=0.02,
        )

        ct = st.session_state.ctype
        if ct == "Candle" and has_ohlc:
            fig.add_trace(go.Candlestick(
                x=df.index,
                open=df["Open"], high=df["High"],
                low=df["Low"],   close=df["Close"],
                increasing_line_color=GRN,
                decreasing_line_color=RED,
                name="OHLC", showlegend=False,
            ), row=1, col=1)
        elif ct == "Area":
            fig.add_trace(go.Scatter(
                x=df.index, y=df["Close"], mode="lines",
                line=dict(color=lc, width=1.5),
                fill="tozeroy", fillcolor=fa,
                name="Price", showlegend=False,
            ), row=1, col=1)
        else:
            fig.add_trace(go.Scatter(
                x=df.index, y=df["Close"], mode="lines",
                line=dict(color=lc, width=1.5),
                name="Price", showlegend=False,
            ), row=1, col=1)

        # MAs
        close_f = df["Close"].astype(float)
        if len(df) >= 20:
            fig.add_trace(go.Scatter(
                x=df.index, y=close_f.rolling(20).mean(),
                mode="lines", line=dict(color="#f59e0b", width=1.2, dash="dot"),
                name="MA20", opacity=0.9,
            ), row=1, col=1)
        if len(df) >= 50:
            fig.add_trace(go.Scatter(
                x=df.index, y=close_f.rolling(50).mean(),
                mode="lines", line=dict(color="#6366f1", width=1.2, dash="dot"),
                name="MA50", opacity=0.9,
            ), row=1, col=1)

        # Volume
        if has_vol:
            o_col = df.get("Open", df["Close"])
            vc = [GRN if float(c) >= float(o) else RED
                  for c, o in zip(df["Close"], o_col)]
            fig.add_trace(go.Bar(
                x=df.index, y=df["Volume"],
                marker_color=vc, opacity=0.5,
                name="Vol", showlegend=False,
            ), row=2, col=1)

        ax  = dict(showgrid=False, zeroline=False, color="#94a3b8",
                   tickfont=dict(family="JetBrains Mono", size=10, color="#94a3b8"),
                   linecolor="#e2e8f0")
        yax = dict(showgrid=True, gridcolor="#f1f5f9", zeroline=False,
                   side="right", color="#94a3b8",
                   tickfont=dict(family="JetBrains Mono", size=10, color="#94a3b8"))

        fig.update_layout(
            paper_bgcolor="rgba(255,255,255,0)",
            plot_bgcolor="rgba(255,255,255,0)",
            margin=dict(l=0, r=4, t=4, b=0),
            height=330,
            showlegend=True,
            legend=dict(
                orientation="h", y=1.05, x=0,
                font=dict(family="JetBrains Mono", size=10, color="#94a3b8"),
                bgcolor="rgba(0,0,0,0)",
            ),
            hovermode="x unified",
            hoverlabel=dict(
                bgcolor="#fff", bordercolor="#e2e8f0",
                font=dict(family="JetBrains Mono", size=11, color="#1e293b"),
            ),
            xaxis=dict(**ax),
            xaxis2=dict(**ax, rangeslider=dict(visible=False)),
            yaxis=dict(**yax),
            yaxis2=dict(showgrid=False, showticklabels=False),
        )
        st.plotly_chart(fig, use_container_width=True,
                        config={"displayModeBar": False})
    else:
        st.markdown('<div style="height:260px;display:flex;align-items:center;justify-content:center;color:#94a3b8;font-size:0.75rem">No chart data available</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Center tabs ──
    ctabs = ["Overview","Fundamentals","Financials","Sectors",
             "🤖 Full AI","📰 News AI","📈 Technical AI","🏛 Fundamental AI","💰 Financial AI"]
    # Row 1: data tabs
    tc1 = st.columns(4)
    data_tabs = ["Overview","Fundamentals","Financials","Sectors"]
    for i, t in enumerate(data_tabs):
        tp = "primary" if st.session_state.ctab == t else "secondary"
        if tc1[i].button(t, key=f"ct_{t}", type=tp):
            st.session_state.ctab = t; st.rerun()
    # Row 2: AI tabs
    tc2 = st.columns(5)
    ai_tabs = ["🤖 Full AI","📰 News AI","📈 Technical AI","🏛 Fundamental AI","💰 Financial AI"]
    for i, t in enumerate(ai_tabs):
        tp = "primary" if st.session_state.ctab == t else "secondary"
        if tc2[i].button(t, key=f"ct_{t}", type=tp):
            st.session_state.ctab = t; st.rerun()

    # ── OVERVIEW ──────────────────────────────────────────────────────────────
    if st.session_state.ctab == "Overview":
        st.markdown('<div class="sct">Key Metrics</div>', unsafe_allow_html=True)
        mcap=info.get("marketCap"); wh52=info.get("fiftyTwoWeekHigh")
        wl52=info.get("fiftyTwoWeekLow"); pe_=info.get("trailingPE")
        fpe=info.get("forwardPE"); eps=info.get("trailingEps")
        dy=info.get("dividendYield"); vol=info.get("volume") or info.get("regularMarketVolume")
        avol=info.get("averageVolume"); beta=info.get("beta"); ptb=info.get("priceToBook")
        wk52pct = round((p-wl52)/(wh52-wl52)*100,1) if (wh52 and wl52 and p and wh52!=wl52) else None

        metrics = [
            ("Market Cap",  finr(mcap),           ""),
            ("52W High",    sv(wh52),              "pos" if p and wh52 and p>=wh52*0.95 else ""),
            ("52W Low",     sv(wl52),              "neg" if p and wl52 and p<=wl52*1.05 else ""),
            ("52W Range",   f"{wk52pct:.0f}%" if wk52pct is not None else "—", ""),
            ("P/E (TTM)",   sv(pe_,"",dec=1),      ""),
            ("Fwd P/E",     sv(fpe,"",dec=1),      ""),
            ("EPS (TTM)",   sv(eps),               ""),
            ("Div Yield",   sv(dy,fmt="pct"),       "pos" if dy and float(dy)>0 else ""),
            ("Volume",      sv(vol,fmt="vol"),      ""),
            ("Avg Volume",  sv(avol,fmt="vol"),     ""),
            ("Beta",        sv(beta,"",dec=2),      ""),
            ("Price/Book",  sv(ptb,"",dec=2),       ""),
        ]
        mc4 = st.columns(4)
        for idx_, (lbl, val, vc) in enumerate(metrics):
            mvc = f"mc-v {vc}".strip()
            with mc4[idx_ % 4]:
                st.markdown(f"""<div class="mc">
                  <div class="mc-l">{lbl}</div>
                  <div class="{mvc}">{val}</div>
                </div>""", unsafe_allow_html=True)

    # ── FUNDAMENTALS ──────────────────────────────────────────────────────────
    elif st.session_state.ctab == "Fundamentals":
        roe=info.get("returnOnEquity"); roa=info.get("returnOnAssets")
        gm=info.get("grossMargins"); om=info.get("operatingMargins")
        pm=info.get("profitMargins"); d2e=info.get("debtToEquity")
        cr=info.get("currentRatio"); fcf=info.get("freeCashflow")
        rev=info.get("totalRevenue"); ebit=info.get("ebitda")
        ni=info.get("netIncomeToCommon"); eg=info.get("earningsGrowth")
        rg=info.get("revenueGrowth"); bv=info.get("bookValue")
        td=info.get("totalDebt"); tc_=info.get("totalCash")
        shr=info.get("sharesOutstanding"); evr=info.get("enterpriseToRevenue")
        eve=info.get("enterpriseToEbitda"); qeg=info.get("earningsQuarterlyGrowth")

        fa2, fb2 = st.columns(2)
        with fa2:
            st.markdown('<div class="sct">Profitability</div>', unsafe_allow_html=True)
            rows1=[
                ("Revenue",          finr(rev)),
                ("EBITDA",           finr(ebit)),
                ("Net Income",       finr(ni)),
                ("Free Cash Flow",   finr(fcf)),
                ("Gross Margin",     sv(gm, fmt="pct")),
                ("Operating Margin", sv(om, fmt="pct")),
                ("Net Margin",       sv(pm, fmt="pct")),
                ("ROE",              sv(roe,fmt="pct")),
                ("ROA",              sv(roa,fmt="pct")),
                ("EV/Revenue",       sv(evr,"",dec=2)),
                ("EV/EBITDA",        sv(eve,"",dec=2)),
                ("Rev Growth YoY",   sv(rg, fmt="pct")),
                ("Earn Growth YoY",  sv(eg, fmt="pct")),
                ("Earn Growth QoQ",  sv(qeg,fmt="pct")),
            ]
            st.markdown('<table class="ft">', unsafe_allow_html=True)
            for lbl, val in rows1:
                st.markdown(f'<tr><td class="fl">{lbl}</td><td class="fv">{val}</td></tr>', unsafe_allow_html=True)
            st.markdown('</table>', unsafe_allow_html=True)

        with fb2:
            st.markdown('<div class="sct">Balance Sheet</div>', unsafe_allow_html=True)
            nd_ = finr(float(td)-float(tc_)) if (td and tc_) else "—"
            rows2=[
                ("Total Debt",        finr(td)),
                ("Total Cash",        finr(tc_)),
                ("Net Debt",          nd_),
                ("Debt/Equity",       sv(d2e,"",dec=2)),
                ("Current Ratio",     sv(cr,"",dec=2)),
                ("Book Value/Share",  sv(bv, dec=2)),
                ("Shares Outstanding",sv(shr,fmt="vol")),
                ("Float Shares",      sv(info.get("floatShares"),fmt="vol")),
            ]
            st.markdown('<table class="ft">', unsafe_allow_html=True)
            for lbl, val in rows2:
                st.markdown(f'<tr><td class="fl">{lbl}</td><td class="fv">{val}</td></tr>', unsafe_allow_html=True)
            st.markdown('</table>', unsafe_allow_html=True)

            st.markdown('<div class="sct" style="margin-top:10px">Company</div>', unsafe_allow_html=True)
            ci = [
                ("Sector",   info.get("sector","—")),
                ("Industry", info.get("industry","—")),
                ("Exchange", info.get("exchange","—")),
                ("Country",  info.get("country","India")),
            ]
            st.markdown('<table class="ft">', unsafe_allow_html=True)
            for lbl, val in ci:
                st.markdown(f'<tr><td class="fl">{lbl}</td><td class="fv">{val}</td></tr>', unsafe_allow_html=True)
            st.markdown('</table>', unsafe_allow_html=True)

        summary = info.get("longBusinessSummary","")
        if summary:
            st.markdown(f'<div style="font-size:0.68rem;color:#64748b;line-height:1.65;margin-top:10px;padding:12px 14px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:7px">{summary[:700]}…</div>', unsafe_allow_html=True)

    # ── FINANCIALS ────────────────────────────────────────────────────────────
    elif st.session_state.ctab == "Financials":
        fin, bs, cf = fget(st.session_state.sel)
        def render_fin(df_in, label):
            if df_in is None or df_in.empty:
                st.markdown(f'<div style="padding:10px;color:#94a3b8;font-size:0.65rem">{label}: not available</div>', unsafe_allow_html=True)
                return
            st.markdown(f'<div class="sct">{label}</div>', unsafe_allow_html=True)
            d = df_in.head(10).copy()
            d.index   = [str(x)[:40] for x in d.index]
            d.columns = [str(c)[:12] for c in d.columns]
            def fc(x):
                try:
                    f=float(x)
                    if abs(f)>=1e7: return f"₹{f/1e7:.1f}Cr"
                    if abs(f)>=1e5: return f"₹{f/1e5:.1f}L"
                    return f"₹{f:,.0f}"
                except: return "—"
            st.dataframe(d.map(fc), use_container_width=True)
        render_fin(fin, "Income Statement (Annual)")
        render_fin(bs,  "Balance Sheet (Annual)")
        render_fin(cf,  "Cash Flow (Annual)")

    # ── SECTORS ───────────────────────────────────────────────────────────────
    elif st.session_state.ctab == "Sectors":
        st.markdown('<div class="sct">Sector Performance Today</div>', unsafe_allow_html=True)
        sc4 = st.columns(4)
        for i, s in enumerate(SECTORS):
            qs = qget(s["sym"]); arr_s, _ = ud(qs["pct"]); cls_s = sc(qs["pct"])
            with sc4[i % 4]:
                st.markdown(f"""<div class="sec-t">
                  <div class="sec-n">{s['name']}</div>
                  <div class="sec-p {cls_s}">{arr_s} {abs(qs['pct']):.2f}%</div>
                </div>""", unsafe_allow_html=True)

        st.markdown('<div class="sct" style="margin-top:14px">1-Month Normalised Return (%)</div>', unsafe_allow_html=True)
        sfig = go.Figure()
        pal  = ["#16a34a","#2563eb","#d97706","#9333ea","#dc2626","#0891b2","#f97316","#65a30d"]
        for si, s in enumerate(SECTORS):
            sdf = hget(s["sym"], "1mo", "1d")
            if not sdf.empty and "Close" in sdf.columns and len(sdf) > 1:
                base = float(sdf["Close"].iloc[0])
                norm = (sdf["Close"].astype(float) / base - 1) * 100
                sfig.add_trace(go.Scatter(
                    x=sdf.index, y=norm.round(2), mode="lines",
                    name=s["name"], line=dict(color=pal[si], width=1.5)))
        sfig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0,r=4,t=4,b=0), height=230,
            hovermode="x unified",
            legend=dict(orientation="h", y=1.1,
                        font=dict(family="JetBrains Mono",size=10,color="#64748b"),
                        bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(showgrid=False, zeroline=False, color="#94a3b8",
                       tickfont=dict(family="JetBrains Mono",size=10,color="#94a3b8")),
            yaxis=dict(showgrid=True, gridcolor="#f1f5f9", zeroline=True,
                       zerolinecolor="#e2e8f0", side="right", ticksuffix="%",
                       tickfont=dict(family="JetBrains Mono",size=10,color="#94a3b8")),
            hoverlabel=dict(bgcolor="#fff", bordercolor="#e2e8f0",
                            font=dict(family="JetBrains Mono",size=11,color="#1e293b")),
        )
        st.plotly_chart(sfig, use_container_width=True, config={"displayModeBar":False})

    # ══════════════ AI ANALYSIS TABS ══════════════════════════════════════════

    # Shared data prep for all AI tabs
    elif st.session_state.ctab in ("🤖 Full AI","📰 News AI","📈 Technical AI","🏛 Fundamental AI","💰 Financial AI"):

        sym_label = st.session_state.sel_name
        ticker    = st.session_state.sel

        # Gather everything once
        tech_df_1y = hget(ticker, "1y", "1d")
        tech_df_1m = hget(ticker, "1mo", "1h")
        technicals = calc_technicals(tech_df_1y)

        # Financials text
        fin_obj, bs_obj, cf_obj = fget(ticker)
        def df_to_text(df_in, label, rows=8):
            if df_in is None or df_in.empty: return f"{label}: not available\n"
            d = df_in.head(rows).copy()
            d.index   = [str(x)[:35] for x in d.index]
            d.columns = [str(c)[:10] for c in d.columns]
            def fc(x):
                try:
                    f=float(x)
                    if abs(f)>=1e7: return f"₹{f/1e7:.1f}Cr"
                    if abs(f)>=1e5: return f"₹{f/1e5:.1f}L"
                    return f"₹{f:,.0f}"
                except: return str(x)
            return f"{label}:\n{d.map(fc).to_string()}\n\n"

        fin_text = df_to_text(fin_obj, "Income Statement")
        bs_text  = df_to_text(bs_obj,  "Balance Sheet")
        cf_text  = df_to_text(cf_obj,  "Cash Flow")

        # News headlines
        arts      = news_get(st.session_state.nkey, f"India NSE BSE {sym_label}") if st.session_state.nkey else []
        news_text = "\n".join([f"- {a.get('title','')} ({a.get('source',{}).get('name','')}, {tago(a.get('publishedAt',''))})"
                               for a in arts[:12]]) if arts else "No news available (add NewsAPI key in sidebar for live news)."

        # Fundamentals dict
        fund_keys = [
            "marketCap","trailingPE","forwardPE","trailingEps","dividendYield",
            "returnOnEquity","returnOnAssets","grossMargins","operatingMargins",
            "profitMargins","debtToEquity","currentRatio","freeCashflow",
            "totalRevenue","ebitda","netIncomeToCommon","earningsGrowth",
            "revenueGrowth","bookValue","priceToBook","beta","fiftyTwoWeekHigh",
            "fiftyTwoWeekLow","enterpriseToRevenue","enterpriseToEbitda",
            "earningsQuarterlyGrowth","sector","industry",
        ]
        fund_dict = {k: info.get(k) for k in fund_keys if info.get(k) is not None}
        fund_text = "\n".join([f"  {k}: {v}" for k,v in fund_dict.items()])

        price_ctx = (f"Current Price: ₹{q['p']:,.2f} | Change: {q['ch']:+.2f} ({q['pct']:+.2f}%) | "
                     f"Open: ₹{op_:,.2f} | High: ₹{hi:,.2f} | Low: ₹{lo:,.2f} | Prev Close: ₹{pc:,.2f}")

        tech_text = "\n".join([f"  {k}: {v}" for k,v in technicals.items()])

        # ── PROMPTS ────────────────────────────────────────────────────────────
        PROMPTS = {
            "🤖 Full AI": f"""You are a senior equity research analyst at a top Indian investment bank. Provide a comprehensive, institutional-quality analysis of {sym_label} ({ticker}).

**TODAY'S PRICE DATA:**
{price_ctx}

**TECHNICAL INDICATORS:**
{tech_text}

**FUNDAMENTALS:**
{fund_text}

**FINANCIAL STATEMENTS SUMMARY:**
{fin_text}{bs_text}{cf_text}

**RECENT NEWS HEADLINES:**
{news_text}

Write a thorough analysis covering:
1. **Executive Summary** – 3-sentence verdict on the stock right now
2. **Price Action & Momentum** – What the charts say, trend direction, key levels
3. **Volume Analysis** – What volume signals about conviction
4. **Technical Setup** – MA positions, RSI, MACD, Bollinger Bands interpretation
5. **Fundamental Quality** – Business quality, margins, return ratios
6. **Valuation** – Is it cheap, fair, or expensive vs. sector/history?
7. **Financial Health** – Balance sheet strength, cash flow quality
8. **News Sentiment** – How recent headlines affect the thesis
9. **Risk Factors** – Key risks to the bull/bear case
10. **Outlook & Verdict** – Bull case, Bear case, and your base case with a clear BUY/HOLD/SELL stance

Be specific with numbers. Be bold with opinions. Write like a Goldman Sachs research note.""",

            "📰 News AI": f"""You are a financial news analyst specialising in Indian equity markets. Analyse the following recent news headlines for {sym_label} ({ticker}) and provide a structured news-driven investment view.

**STOCK CONTEXT:**
{price_ctx}
Sector: {info.get('sector','—')} | Industry: {info.get('industry','—')}

**RECENT NEWS HEADLINES:**
{news_text}

Provide:
1. **News Sentiment Score** – Overall: Bullish / Neutral / Bearish, and why
2. **Key Themes** – What are the 2-3 dominant narratives across these headlines?
3. **Catalysts Identified** – Any near-term positive or negative catalysts visible?
4. **Market Reaction Assessment** – Are headlines reflected in the current price or is there a divergence?
5. **Credibility & Source Quality** – Are these from reliable sources? Any conflicting reports?
6. **Trading Implication** – What should a trader / investor do based purely on this news flow?

If no news is available, provide context on what news would be most important to watch for this type of company.""",

            "📈 Technical AI": f"""You are a professional technical analyst with 20 years of experience in Indian equity markets (NSE/BSE). Analyse the following technical data for {sym_label} ({ticker}) and provide a rigorous, actionable technical analysis.

**CURRENT PRICE DATA:**
{price_ctx}

**TECHNICAL INDICATORS:**
{tech_text}

Provide a detailed technical analysis:
1. **Trend Analysis** – What is the primary trend (daily, weekly)? Is it intact or reversing?
2. **Moving Average Analysis** – Price vs MA20/50/200 — bullish/bearish cross signals, golden/death cross?
3. **RSI Analysis** – Is the stock overbought, oversold, or neutral? Divergence present?
4. **MACD Analysis** – Crossover signals, histogram trend, momentum acceleration/deceleration
5. **Bollinger Band Analysis** – Squeeze, expansion, breakout, or mean-reversion signal?
6. **Volume Analysis** – Is the current move confirmed by volume? Volume spike or drought?
7. **Volatility** – Annualised volatility context — is this a high or low volatility phase?
8. **Key Levels** – Identify immediate support and resistance levels from the data
9. **Return Analysis** – 1M/3M/6M returns in context
10. **Trading Signal** – Clear BULLISH / BEARISH / NEUTRAL signal with confidence level (High/Medium/Low) and suggested entry zone, stop loss, target""",

            "🏛 Fundamental AI": f"""You are a fundamental equity analyst specialising in Indian listed companies. Provide a deep fundamental analysis of {sym_label} ({ticker}).

**CURRENT MARKET DATA:**
{price_ctx}

**FUNDAMENTAL DATA:**
{fund_text}

**FINANCIAL STATEMENTS:**
{fin_text}{bs_text}

Provide a rigorous fundamental analysis:
1. **Business Quality Assessment** – What do margins, ROE, and ROA say about the quality of this business?
2. **Growth Analysis** – Revenue and earnings growth trajectory — accelerating or decelerating?
3. **Profitability Deep Dive** – Gross, operating, and net margin trends and what they imply
4. **Valuation Analysis** – P/E, Forward P/E, P/B, EV/EBITDA, EV/Revenue vs. sector norms
5. **Balance Sheet Health** – Debt levels, liquidity, financial leverage risk
6. **Capital Efficiency** – ROE decomposition (DuPont), asset turnover, free cash flow generation
7. **Dividend & Capital Allocation** – Dividend yield, payout policy, buybacks
8. **Competitive Position** – What do these numbers suggest about the company's moat?
9. **Relative Value** – Cheap, fair value, or overvalued based purely on fundamentals?
10. **Fundamental Verdict** – STRONG BUY / BUY / HOLD / REDUCE / SELL with key thesis

Use specific numbers from the data provided. Benchmark against Indian market averages where relevant.""",

            "💰 Financial AI": f"""You are a CFA-qualified financial statement analyst. Conduct a thorough financial statement analysis of {sym_label} ({ticker}) based on the following data.

**MARKET CONTEXT:**
{price_ctx}
Market Cap: {finr(info.get('marketCap'))} | Sector: {info.get('sector','—')}

**INCOME STATEMENT:**
{fin_text}

**BALANCE SHEET:**
{bs_text}

**CASH FLOW STATEMENT:**
{cf_text}

**KEY RATIOS FROM FINANCIALS:**
{fund_text}

Provide a comprehensive financial statement analysis:
1. **Revenue Quality** – Revenue growth, consistency, and sustainability
2. **Earnings Quality** – Is net income of high quality? Cash conversion, accruals analysis
3. **Margin Trajectory** – Are margins expanding, contracting, or stable? Why?
4. **EBITDA Analysis** – EBITDA quality, cash conversion, capex intensity
5. **Free Cash Flow Analysis** – FCF generation, FCF yield, capex vs. depreciation
6. **Working Capital** – Working capital trends, days sales outstanding, inventory days
7. **Debt & Leverage** – Debt structure, interest coverage, net debt/EBITDA
8. **Return on Capital** – ROCE, ROE, ROA trends year-over-year
9. **Red Flags** – Any accounting concerns, aggressive recognition, or balance sheet risks?
10. **Financial Health Score** – Rate the financial health 1-10 with justification and overall verdict

Be forensic. Flag any inconsistencies between the income statement, balance sheet, and cash flow."""
        }

        active_ai = st.session_state.ctab
        badge_map = {
            "🤖 Full AI":        ("ai-badge-full",  "🤖 Full Stock Analysis"),
            "📰 News AI":        ("ai-badge-news",  "📰 News & Sentiment"),
            "📈 Technical AI":   ("ai-badge-tech",  "📈 Technical Analysis"),
            "🏛 Fundamental AI": ("ai-badge-fund",  "🏛 Fundamental Analysis"),
            "💰 Financial AI":   ("ai-badge-fin",   "💰 Financial Statement Analysis"),
        }
        badge_cls, title = badge_map[active_ai]
        cache_key = f"ai_{active_ai}_{ticker}"

        st.markdown(f"""<div class="ai-card">
          <div class="ai-card-header">
            <span class="ai-badge {badge_cls}">{active_ai}</span>
            <span class="ai-card-title">{title} — {sym_label}</span>
          </div>
        """, unsafe_allow_html=True)

        # Show cached result or generate button
        if cache_key in st.session_state:
            st.markdown(f'<div class="ai-body">{st.session_state[cache_key]}</div>', unsafe_allow_html=True)
            col_a, col_b = st.columns([1,4])
            with col_a:
                if st.button("↺ Regenerate", key=f"regen_{cache_key}"):
                    del st.session_state[cache_key]
                    st.rerun()
        else:
            if active_ai == "📰 News AI" and not arts:
                st.markdown('<div style="font-size:0.72rem;color:#94a3b8;padding:8px 0">Add your NewsAPI key in the sidebar to enable news-based AI analysis.</div>', unsafe_allow_html=True)
            if st.button(f"✦ Generate {title}", key=f"gen_{cache_key}", type="primary"):
                with st.spinner("Analysing with Claude AI…"):
                    result = call_claude(PROMPTS[active_ai])
                st.session_state[cache_key] = result
                st.rerun()

        st.markdown('<div class="ai-disclaimer">⚠ AI-generated analysis is for informational purposes only. Not financial advice. Always do your own research before investing.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════ RIGHT ═════════════════════════════════════
with R:
    RTABS = ["Gainers","Losers","Indices","Commodities","MCX"]
    rtc   = st.columns(len(RTABS))
    for i, t in enumerate(RTABS):
        tp = "primary" if st.session_state.rtab == t else "secondary"
        if rtc[i].button(t, key=f"rt_{t}", type=tp):
            st.session_state.rtab = t; st.rerun()

    tab = st.session_state.rtab

    if tab in ("Gainers","Losers"):
        rows = []
        for sym in NIFTY50:
            qr   = qget(sym); base = sym.replace(".NS","")
            rows.append({"sym":base,"full":sym,
                         "name":NSE_STOCKS.get(base,base),
                         "p":qr["p"],"pct":qr["pct"]})
        rows.sort(key=lambda x: x["pct"], reverse=(tab=="Gainers"))
        for r in rows[:20]:
            arr_r, _ = ud(r["pct"]); cls_r = sc(r["pct"])
            ps  = f"₹{r['p']:,.2f}" if r["p"] else "—"
            sel = "rr rr-sel" if r["full"] == st.session_state.sel else "rr"
            st.markdown(f"""<div class="{sel}">
              <div>
                <div class="rr-sym">{r['sym']}</div>
                <div class="rr-nm">{r['name'][:24]}</div>
              </div>
              <div>
                <div class="rr-p">{ps}</div>
                <div class="rr-c {cls_r}">{arr_r} {abs(r['pct']):.2f}%</div>
              </div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"Select {r['sym']}", key=f"rsel_{tab}_{r['sym']}", use_container_width=True):
                st.session_state.sel      = r["full"]
                st.session_state.sel_name = r["name"]
                st.rerun()

    elif tab == "Indices":
        for ix in ALL_IDX:
            qi = qget(ix["sym"]); arr_i, _ = ud(qi["pct"]); cls_i = sc(qi["pct"])
            ps  = f"{qi['p']:,.2f}" if qi["p"] else "—"
            sel = "rr rr-sel" if ix["sym"] == st.session_state.sel else "rr"
            st.markdown(f"""<div class="{sel}">
              <div><div class="rr-sym">{ix['name']}</div></div>
              <div>
                <div class="rr-p">{ps}</div>
                <div class="rr-c {cls_i}">{arr_i} {abs(qi['pct']):.2f}%</div>
              </div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"Select {ix['name'][:16]}", key=f"ri_{ix['sym']}", use_container_width=True):
                st.session_state.sel      = ix["sym"]
                st.session_state.sel_name = ix["name"]
                st.rerun()

    elif tab == "Commodities":
        for c in COMMODITIES:
            qc = qget(c["sym"]); arr_c, _ = ud(qc["pct"]); cls_c = sc(qc["pct"])
            ps  = f"{qc['p']:,.2f}" if qc["p"] else "—"
            sel = "rr rr-sel" if c["sym"] == st.session_state.sel else "rr"
            st.markdown(f"""<div class="{sel}">
              <div><div class="rr-sym">{c['name']}</div></div>
              <div>
                <div class="rr-p">{ps}</div>
                <div class="rr-c {cls_c}">{arr_c} {abs(qc['pct']):.2f}%</div>
              </div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"Select {c['name'][:16]}", key=f"rc_{c['sym']}", use_container_width=True):
                st.session_state.sel      = c["sym"]
                st.session_state.sel_name = c["name"]
                st.rerun()

    elif tab == "MCX":
        for m in MCX_LIST:
            qm = qget(m["sym"]); arr_m, _ = ud(qm["pct"]); cls_m = sc(qm["pct"])
            bm  = m["sym"].replace(".NS","")
            ps  = f"₹{qm['p']:,.2f}" if qm["p"] else "—"
            sel = "rr rr-sel" if m["sym"] == st.session_state.sel else "rr"
            st.markdown(f"""<div class="{sel}">
              <div>
                <div class="rr-sym">{bm}</div>
                <div class="rr-nm">{m['name']}</div>
              </div>
              <div>
                <div class="rr-p">{ps}</div>
                <div class="rr-c {cls_m}">{arr_m} {abs(qm['pct']):.2f}%</div>
              </div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"Select {bm[:16]}", key=f"rm_{m['sym']}", use_container_width=True):
                st.session_state.sel      = m["sym"]
                st.session_state.sel_name = m["name"]
                st.rerun()

    # ── Mini sparkline ──
    st.markdown("<hr style='border:none;border-top:1px solid #f1f5f9;margin:6px 0'>", unsafe_allow_html=True)
    mdf = hget(st.session_state.sel, "1mo", "1d")
    if not mdf.empty and "Close" in mdf.columns:
        lc_m = GRN if pct >= 0 else RED
        fa_m = "rgba(22,163,74,0.1)" if pct >= 0 else "rgba(220,38,38,0.1)"
        mfig = go.Figure(go.Scatter(
            x=mdf.index, y=mdf["Close"].astype(float),
            mode="lines", line=dict(color=lc_m, width=1.5),
            fill="tozeroy", fillcolor=fa_m,
        ))
        mfig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0,r=0,t=0,b=0), height=55,
            showlegend=False,
            xaxis=dict(visible=False), yaxis=dict(visible=False),
        )
        slbl = st.session_state.sel.replace(".NS","").replace(".BO","")
        st.markdown(f'<div style="font-size:0.56rem;color:#94a3b8;padding:3px 8px;font-family:JetBrains Mono,monospace;text-transform:uppercase;letter-spacing:0.1em">{slbl} · 1M</div>', unsafe_allow_html=True)
        st.plotly_chart(mfig, use_container_width=True, config={"displayModeBar":False})

    st.markdown("<hr style='border:none;border-top:1px solid #f1f5f9;margin:6px 0'>", unsafe_allow_html=True)
    if st.button("⟳  Refresh Data", use_container_width=True):
        st.cache_data.clear(); st.rerun()
    st.markdown('<div style="font-size:0.54rem;color:#cbd5e1;text-align:center;padding:4px;font-family:JetBrains Mono,monospace">Yahoo Finance · 2 min cache · ~15 min delay</div>', unsafe_allow_html=True)
