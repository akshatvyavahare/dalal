import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timezone, timedelta
import requests
import streamlit.components.v1 as components

st.set_page_config(page_title="Dalal Terminal", page_icon="◈",
                   layout="wide", initial_sidebar_state="collapsed")

IST = timezone(timedelta(hours=5, minutes=30))

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
    "BANDHANBNK":"Bandhan Bank","BRITANNIA":"Britannia Industries",
    "CANBK":"Canara Bank","CHOLAFIN":"Cholamandalam Finance","CIPLA":"Cipla",
    "COLPAL":"Colgate-Palmolive","DABUR":"Dabur India",
    "DIVISLAB":"Divi's Laboratories","DLF":"DLF",
    "DRREDDY":"Dr. Reddy's Laboratories","EICHERMOT":"Eicher Motors",
    "FEDERALBNK":"Federal Bank","GAIL":"GAIL India",
    "GODREJCP":"Godrej Consumer","HDFCAMC":"HDFC AMC",
    "HDFCLIFE":"HDFC Life Insurance","HEROMOTOCO":"Hero MotoCorp",
    "HINDZINC":"Hindustan Zinc","IDFCFIRSTB":"IDFC First Bank",
    "INDHOTEL":"Indian Hotels","INDIGO":"IndiGo","INDUSINDBK":"IndusInd Bank",
    "IRCTC":"IRCTC","JSWENERGY":"JSW Energy","JUBLFOOD":"Jubilant FoodWorks",
    "LICI":"LIC India","LTIM":"LTIMindtree","LUPIN":"Lupin",
    "M&M":"Mahindra & Mahindra","MARICO":"Marico","MPHASIS":"Mphasis",
    "MRF":"MRF","MUTHOOTFIN":"Muthoot Finance","NAUKRI":"Info Edge (Naukri)",
    "NMDC":"NMDC","OFSS":"Oracle Financial Services","PAGEIND":"Page Industries",
    "PERSISTENT":"Persistent Systems","PETRONET":"Petronet LNG",
    "PFC":"Power Finance Corp","PIDILITIND":"Pidilite Industries",
    "PNB":"Punjab National Bank","POLYCAB":"Polycab India",
    "RECLTD":"REC Limited","SAIL":"SAIL","SHREECEM":"Shree Cement",
    "SIEMENS":"Siemens India","SRF":"SRF Limited","SRTRANSFIN":"Shriram Finance",
    "TATACOMM":"Tata Communications","TATACONSUM":"Tata Consumer Products",
    "TATAELXSI":"Tata Elxsi","TATAPOWER":"Tata Power",
    "TORNTPHARM":"Torrent Pharmaceuticals","TRENT":"Trent","TVSMOTOR":"TVS Motor",
    "UBL":"United Breweries","UNIONBANK":"Union Bank of India","UPL":"UPL",
    "VEDL":"Vedanta","VOLTAS":"Voltas","YESBANK":"Yes Bank","ZOMATO":"Zomato",
    "PAYTM":"Paytm","NYKAA":"Nykaa","DELHIVERY":"Delhivery",
    "MANKIND":"Mankind Pharma","HAL":"HAL","HAVELLS":"Havells India",
    "LODHA":"Macrotech (Lodha)","MAXHEALTH":"Max Healthcare","MCX":"MCX India",
    "PHOENIXLTD":"Phoenix Mills","PRESTIGE":"Prestige Estates",
    "VBL":"Varun Beverages","PIIND":"PI Industries",
    "BALKRISIND":"Balkrishna Industries","DEEPAKNTR":"Deepak Nitrite",
    "IRFC":"IRFC","LICHSGFIN":"LIC Housing Finance","LTTS":"L&T Tech Services",
    "RBLBANK":"RBL Bank","SCHAEFFLER":"Schaeffler India",
    "SUNDARMFIN":"Sundaram Finance","SUPREMEIND":"Supreme Industries",
    "TANLA":"Tanla Platforms","TIINDIA":"Tube Investments",
    "ZYDUSLIFE":"Zydus Lifesciences","KPITTECH":"KPIT Technologies",
    "KAYNES":"Kaynes Technology","MAPMYINDIA":"MapmyIndia",
}

INDICES = [
    {"sym":"^NSEI","name":"NIFTY 50","tv":"NSE:NIFTY"},
    {"sym":"^BSESN","name":"SENSEX","tv":"BSE:SENSEX"},
    {"sym":"^CNXBANK","name":"BANK NIFTY","tv":"NSE:BANKNIFTY"},
    {"sym":"^CNXIT","name":"NIFTY IT","tv":"NSE:CNXIT"},
    {"sym":"^NSMIDCP","name":"NIFTY MID","tv":"NSE:NIFTY_MIDCAP_100"},
]

MARKETS_TABLE = [
    {"name":"NIFTY 50",  "sym":"^NSEI",    "country":"🇮🇳","tv":"NSE:NIFTY"},
    {"name":"SENSEX",    "sym":"^BSESN",   "country":"🇮🇳","tv":"BSE:SENSEX"},
    {"name":"BANK NIFTY","sym":"^CNXBANK", "country":"🇮🇳","tv":"NSE:BANKNIFTY"},
    {"name":"NIFTY IT",  "sym":"^CNXIT",   "country":"🇮🇳","tv":"NSE:CNXIT"},
    {"name":"NIFTY MID", "sym":"^NSMIDCP", "country":"🇮🇳","tv":"NSE:NIFTY_MIDCAP_100"},
    {"name":"NIFTY PHARMA","sym":"^CNXPHARMA","country":"🇮🇳","tv":"NSE:CNXPHARMA"},
    {"name":"USD/INR",   "sym":"USDINR=X", "country":"💱","tv":"FX_IDC:USDINR"},
    {"name":"Gold",      "sym":"GC=F",     "country":"🥇","tv":"COMEX:GC1!"},
    {"name":"Crude Oil", "sym":"CL=F",     "country":"🛢️","tv":"NYMEX:CL1!"},
]

SECTORS = [
    {"sym":"^CNXIT","name":"IT","tv":"NSE:CNXIT"},
    {"sym":"^CNXBANK","name":"Banking","tv":"NSE:BANKNIFTY"},
    {"sym":"^CNXPHARMA","name":"Pharma","tv":"NSE:CNXPHARMA"},
    {"sym":"^CNXFMCG","name":"FMCG","tv":"NSE:CNXFMCG"},
    {"sym":"^CNXAUTO","name":"Auto","tv":"NSE:CNXAUTO"},
    {"sym":"^CNXREALTY","name":"Realty","tv":"NSE:CNXREALTY"},
    {"sym":"^CNXMETAL","name":"Metal","tv":"NSE:CNXMETAL"},
    {"sym":"^CNXENERGY","name":"Energy","tv":"NSE:CNXENERGY"},
    {"sym":"^CNXINFRA","name":"Infra","tv":"NSE:CNXINFRA"},
    {"sym":"^CNXPSUBANK","name":"PSU Bank","tv":"NSE:CNXPSUBANK"},
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

NAV_ITEMS = [
    ("📊","Dashboard"),("📈","Market Data"),("🔍","Stock Screener"),
    ("💼","Portfolio"),("🔔","Alerts"),("⚙️","Settings"),
]

# ── SESSION STATE ──────────────────────────────────────────────────────────────
def ss(k,v):
    if k not in st.session_state: st.session_state[k]=v

ss("page","Market Data")
ss("watchlist",[
    {"sym":"RELIANCE.NS","name":"Reliance Industries","tv":"NSE:RELIANCE"},
    {"sym":"TCS.NS","name":"Tata Consultancy Services","tv":"NSE:TCS"},
    {"sym":"HDFCBANK.NS","name":"HDFC Bank","tv":"NSE:HDFCBANK"},
    {"sym":"INFY.NS","name":"Infosys","tv":"NSE:INFY"},
    {"sym":"ICICIBANK.NS","name":"ICICI Bank","tv":"NSE:ICICIBANK"},
    {"sym":"SBIN.NS","name":"State Bank of India","tv":"NSE:SBIN"},
])
ss("sel","RELIANCE.NS"); ss("sel_name","Reliance Industries")
ss("sel_tv","NSE:RELIANCE"); ss("nkey","")
ss("chart_interval","D"); ss("portfolio",[])
ss("alert_sym",""); ss("alert_price","")

# ── DATA ──────────────────────────────────────────────────────────────────────
def to_sym(raw):
    r=raw.strip().upper()
    if any(r.endswith(s) for s in [".NS",".BO","=F","=X"]) or r.startswith("^"): return r
    return r+".NS"

def to_tv(sym):
    base=sym.replace(".NS","").replace(".BO","")
    return f"NSE:{base}"

@st.cache_data(ttl=120,show_spinner=False)
def qget(sym):
    try:
        fi=yf.Ticker(sym).fast_info
        p=round(float(fi.last_price or 0),2)
        pc=round(float(fi.previous_close or 0),2)
        ch=round(p-pc,2); pct=round((ch/pc*100) if pc else 0,2)
        return {"p":p,"pc":pc,"ch":ch,"pct":pct,
                "hi":round(float(fi.day_high or 0),2),
                "lo":round(float(fi.day_low  or 0),2),
                "vol":int(fi.three_month_average_volume or 0)}
    except: return {"p":0,"pc":0,"ch":0,"pct":0,"hi":0,"lo":0,"vol":0}

@st.cache_data(ttl=300,show_spinner=False)
def iget(sym):
    try: return yf.Ticker(sym).info or {}
    except: return {}

@st.cache_data(ttl=300,show_spinner=False)
def news_get(key,q):
    if not key: return []
    try:
        r=requests.get("https://newsapi.org/v2/everything",
            params={"q":q,"apiKey":key,"sortBy":"publishedAt","pageSize":20,"language":"en"},timeout=8)
        d=r.json(); return d.get("articles",[]) if d.get("status")=="ok" else []
    except: return []

@st.cache_data(ttl=300,show_spinner=False)
def ai_summary(api_key, context):
    if not api_key: return ""
    try:
        r=requests.post("https://api.anthropic.com/v1/messages",
            headers={"x-api-key":api_key,"anthropic-version":"2023-06-01","content-type":"application/json"},
            json={"model":"claude-sonnet-4-20250514","max_tokens":300,
                  "messages":[{"role":"user","content":f"Write a 3-sentence market summary for Indian markets today based on this data: {context}. Be concise and professional."}]},
            timeout=15)
        d=r.json()
        return d["content"][0]["text"] if d.get("content") else ""
    except: return ""

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
        if abs(v)>=1e12: return f"₹{v/1e12:.2f}T"
        if abs(v)>=1e9:  return f"₹{v/1e9:.2f}B"
        if abs(v)>=1e7:  return f"₹{v/1e7:.1f}Cr"
        if abs(v)>=1e5:  return f"₹{v/1e5:.1f}L"
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

def do_search(q):
    q=q.strip().upper()
    if len(q)<2: return []
    return [{"sym":k,"name":v} for k,v in NSE_STOCKS.items()
            if q in k or q in v.upper()][:8]

now_ist = datetime.now(IST)
now_str = now_ist.strftime("%d %b %Y  %H:%M IST")

# ── TRADINGVIEW WIDGET ─────────────────────────────────────────────────────────
def tv_chart(symbol, height=500, interval="D", theme="light"):
    html = f"""
    <div class="tradingview-widget-container" style="height:{height}px;width:100%">
      <div id="tv_chart_{symbol.replace(':','_').replace('/','_')}" style="height:100%;width:100%"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({{
        "autosize": true,
        "symbol": "{symbol}",
        "interval": "{interval}",
        "timezone": "Asia/Kolkata",
        "theme": "{theme}",
        "style": "1",
        "locale": "en",
        "toolbar_bg": "#f8fafc",
        "enable_publishing": false,
        "hide_side_toolbar": false,
        "allow_symbol_change": true,
        "studies": ["RSI@tv-basicstudies","MACD@tv-basicstudies","BB@tv-basicstudies"],
        "container_id": "tv_chart_{symbol.replace(':','_').replace('/','_')}",
        "withdateranges": true,
        "hide_top_toolbar": false,
        "save_image": false,
        "details": true,
        "hotlist": false,
        "calendar": false
      }});
      </script>
    </div>
    """
    return html

def tv_mini(symbol, height=80):
    html = f"""
    <div class="tradingview-widget-container" style="height:{height}px;width:100%">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-mini-symbol-overview.js" async>
      {{
        "symbol": "{symbol}",
        "width": "100%",
        "height": "{height}",
        "locale": "en",
        "dateRange": "1D",
        "colorTheme": "light",
        "isTransparent": true,
        "autosize": true,
        "largeChartUrl": "",
        "noTimeScale": true,
        "chartOnly": true
      }}
      </script>
    </div>
    """
    return html

def tv_ticker_tape():
    syms = [{"proName":"NSE:NIFTY","title":"NIFTY"},{"proName":"BSE:SENSEX","title":"SENSEX"},
            {"proName":"NSE:BANKNIFTY","title":"BANK NIFTY"},{"proName":"NSE:CNXIT","title":"NIFTY IT"},
            {"proName":"NSE:RELIANCE","title":"RELIANCE"},{"proName":"NSE:TCS","title":"TCS"},
            {"proName":"NSE:HDFCBANK","title":"HDFC Bank"},{"proName":"NSE:INFY","title":"INFY"},
            {"proName":"NSE:ICICIBANK","title":"ICICI Bank"},{"proName":"NSE:SBIN","title":"SBI"},
            {"proName":"FX_IDC:USDINR","title":"USD/INR"},{"proName":"COMEX:GC1!","title":"Gold"},
            {"proName":"NYMEX:CL1!","title":"Crude Oil"}]
    import json
    html = f"""
    <div class="tradingview-widget-container" style="width:100%">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
      {{
        "symbols": {json.dumps(syms)},
        "showSymbolLogo": false,
        "colorTheme": "light",
        "isTransparent": true,
        "displayMode": "compact",
        "locale": "en"
      }}
      </script>
    </div>
    """
    return html

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body,[class*="css"]{font-family:'Inter',sans-serif;background:#f5f7fa!important;color:#1e293b}
.main .block-container{padding:0!important;max-width:100%!important}
section[data-testid="stSidebar"]{display:none!important}
#MainMenu,footer,header,[data-testid="stToolbar"],.stDeployButton{display:none!important}
::-webkit-scrollbar{width:3px;background:transparent}
::-webkit-scrollbar-thumb{background:#e2e8f0;border-radius:4px}

/* ── LAYOUT COLUMNS ── */
[data-testid="column"]{padding:0!important}

/* Left sidebar column */
[data-testid="column"]:nth-of-type(1) > div:first-child{
  background:#ffffff;
  border-right:1px solid #f1f5f9;
  min-height:100vh;
  padding-bottom:20px;
}

/* Main content column */
[data-testid="column"]:nth-of-type(2) > div:first-child{
  background:#f5f7fa;
  min-height:100vh;
  padding:0;
}

/* ── TICKER TAPE ── */
.ticker-wrap{
  background:#fff;
  border-bottom:1px solid #f1f5f9;
  padding:0;
  height:46px;
  overflow:hidden;
}

/* ── SIDEBAR ── */
.sb-logo{
  padding:20px 20px 16px;
  display:flex;align-items:center;gap:10px;
  border-bottom:1px solid #f8fafc;
}
.sb-logo-icon{
  width:32px;height:32px;border-radius:8px;
  background:#f97316;display:flex;align-items:center;justify-content:center;
  color:#fff;font-size:1rem;font-weight:700;flex-shrink:0;
}
.sb-logo-text{font-size:1rem;font-weight:700;color:#0f172a;letter-spacing:-0.01em}
.sb-logo-sub{font-size:0.6rem;color:#94a3b8;letter-spacing:0.04em}

.sb-section{
  font-size:0.58rem;font-weight:600;color:#94a3b8;
  letter-spacing:0.12em;text-transform:uppercase;
  padding:14px 20px 6px;
}

.sb-nav-item{
  display:flex;align-items:center;gap:10px;
  padding:8px 20px;font-size:0.8rem;color:#64748b;
  cursor:pointer;border-radius:0;transition:all 0.12s;
  border-left:3px solid transparent;
}
.sb-nav-item:hover{background:#f8fafc;color:#1e293b}
.sb-nav-item.active{background:#fff7ed;color:#f97316;border-left:3px solid #f97316;font-weight:500}
.sb-nav-icon{font-size:0.85rem;width:18px;text-align:center}

.sb-divider{height:1px;background:#f8fafc;margin:8px 0}

/* ── WATCHLIST IN SIDEBAR ── */
.sb-wl-hdr{
  padding:8px 20px 6px;
  display:flex;align-items:center;justify-content:space-between;
}
.sb-wl-title{font-size:0.58rem;font-weight:600;color:#94a3b8;letter-spacing:0.12em;text-transform:uppercase}
.sb-wl-add{font-size:0.7rem;color:#94a3b8;cursor:pointer;padding:1px 5px;
  border:1px solid #e2e8f0;border-radius:4px;transition:all 0.1s;background:#f8fafc;line-height:1.4}
.sb-wl-add:hover{color:#f97316;border-color:#f97316;background:#fff7ed}

.wl-chip{
  display:flex;align-items:center;gap:8px;
  padding:6px 20px;cursor:pointer;transition:background 0.1s;
}
.wl-chip:hover{background:#f8fafc}
.wl-chip.active{background:#fff7ed}
.wl-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}
.wl-dot.pos{background:#16a34a}
.wl-dot.neg{background:#dc2626}
.wl-n{font-size:0.75rem;font-weight:500;color:#1e293b;flex:1;min-width:0;
  overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.wl-p{font-size:0.7rem;font-weight:500;font-family:'JetBrains Mono',monospace}
.wl-p.pos{color:#16a34a}.wl-p.neg{color:#dc2626}

/* ── MAIN CONTENT HEADER ── */
.page-header{
  padding:16px 24px 0;
  display:flex;align-items:center;justify-content:space-between;
}
.page-title{font-size:1.2rem;font-weight:700;color:#0f172a;letter-spacing:-0.02em}
.page-sub{font-size:0.72rem;color:#94a3b8;margin-top:2px}
.header-time{
  font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#94a3b8;
  display:flex;align-items:center;gap:8px;
}
.live-badge{
  background:#f0fdf4;border:1px solid #bbf7d0;color:#16a34a;
  font-size:0.6rem;padding:2px 8px;border-radius:20px;font-weight:500;
  display:flex;align-items:center;gap:4px;
}

/* ── CARD ── */
.card{
  background:#fff;border:1px solid #f1f5f9;border-radius:10px;
  padding:18px 20px;margin-bottom:14px;
  box-shadow:0 1px 3px rgba(0,0,0,0.04);
}
.card-title{font-size:0.85rem;font-weight:600;color:#0f172a;margin-bottom:4px}
.card-sub{font-size:0.68rem;color:#94a3b8}

/* ── MARKETS TABLE ── */
.mkt-table{width:100%;border-collapse:collapse}
.mkt-table th{
  font-size:0.62rem;font-weight:600;color:#94a3b8;text-transform:uppercase;
  letter-spacing:0.08em;padding:8px 12px;border-bottom:1px solid #f1f5f9;
  text-align:left;background:#fff;
}
.mkt-table th:last-child,.mkt-table th:nth-child(n+4){text-align:right}
.mkt-table td{
  padding:10px 12px;border-bottom:1px solid #f8fafc;
  font-size:0.78rem;vertical-align:middle;
}
.mkt-table tr:last-child td{border-bottom:none}
.mkt-table tr:hover td{background:#fef9f5;cursor:pointer}
.mkt-name{font-weight:500;color:#1e293b}
.mkt-tag{font-size:0.62rem;color:#94a3b8;background:#f8fafc;
  padding:1px 5px;border-radius:3px;margin-left:5px;font-weight:400}
.mkt-price{font-family:'JetBrains Mono',monospace;font-size:0.78rem;font-weight:500;color:#1e293b;text-align:right}
.mkt-chg{font-family:'JetBrains Mono',monospace;font-size:0.72rem;font-weight:500;text-align:right}
.mkt-chg.pos{color:#16a34a}.mkt-chg.neg{color:#dc2626}
.mkt-pe{font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#64748b;text-align:right}
.mkt-vol{font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#64748b;text-align:right}

/* ── SECTOR BARS ── */
.sec-row{
  display:flex;align-items:center;padding:8px 0;
  border-bottom:1px solid #f8fafc;gap:12px;
}
.sec-row:last-child{border-bottom:none}
.sec-name{font-size:0.75rem;color:#374151;width:100px;flex-shrink:0}
.sec-pct{font-family:'JetBrains Mono',monospace;font-size:0.72rem;font-weight:600;width:54px;flex-shrink:0}
.sec-pct.pos{color:#16a34a}.sec-pct.neg{color:#dc2626}
.sec-bar-wrap{flex:1;background:#f1f5f9;border-radius:3px;height:6px;overflow:hidden}
.sec-bar-inner{height:100%;border-radius:3px;transition:width 0.3s}
.sec-bar-inner.pos{background:#16a34a}
.sec-bar-inner.neg{background:#dc2626}

/* ── NEWS CARD ── */
.news-c{
  display:flex;gap:12px;padding:14px 0;
  border-bottom:1px solid #f8fafc;cursor:pointer;transition:background 0.1s;
}
.news-c:last-child{border-bottom:none}
.news-c:hover{background:#fef9f5;margin:0 -20px;padding:14px 20px}
.news-logo{
  width:36px;height:36px;border-radius:8px;flex-shrink:0;
  display:flex;align-items:center;justify-content:center;
  font-weight:700;font-size:0.75rem;color:#fff;
}
.news-body{flex:1;min-width:0}
.news-src-row{display:flex;align-items:center;justify-content:space-between;margin-bottom:4px}
.news-src{font-size:0.68rem;font-weight:600;color:#0f172a}
.news-time{font-size:0.62rem;color:#94a3b8;font-family:'JetBrains Mono',monospace}
.news-title{font-size:0.76rem;color:#374151;line-height:1.45}
.news-desc{font-size:0.68rem;color:#94a3b8;line-height:1.4;margin-top:3px;
  overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}

/* ── OHLC BAR ── */
.ohlc-bar{
  display:flex;gap:6px;flex-wrap:wrap;margin:8px 0 12px;
}
.otag{background:#f8fafc;border:1px solid #f1f5f9;border-radius:5px;
  padding:4px 10px;font-family:'JetBrains Mono',monospace;font-size:0.64rem}
.ol{color:#94a3b8;margin-right:3px}
.ov{color:#1e293b;font-weight:600}.ov-g{color:#16a34a;font-weight:600}.ov-r{color:#dc2626;font-weight:600}

/* ── METRIC CARD ── */
.mc{background:#f8fafc;border:1px solid #f1f5f9;border-radius:7px;padding:9px 11px}
.mc-l{font-size:0.54rem;font-weight:500;color:#94a3b8;text-transform:uppercase;letter-spacing:0.08em}
.mc-v{font-family:'JetBrains Mono',monospace;font-size:0.82rem;font-weight:600;color:#1e293b;margin-top:4px}
.mc-v.pos{color:#16a34a}.mc-v.neg{color:#dc2626}

/* ── FUND TABLE ── */
.ft{width:100%;border-collapse:collapse}
.ft td{padding:6px 8px;border-bottom:1px solid #f8fafc;font-size:0.7rem}
.ft tr:hover td{background:#fef9f5}
.fl{color:#64748b;font-size:0.65rem}.fv{color:#1e293b;text-align:right;font-family:'JetBrains Mono',monospace;font-size:0.7rem;font-weight:500}

/* ── SCREENER TABLE ── */
.scr-table{width:100%;border-collapse:collapse}
.scr-table th{font-size:0.6rem;font-weight:600;color:#94a3b8;text-transform:uppercase;
  letter-spacing:0.08em;padding:8px 10px;border-bottom:1px solid #f1f5f9;text-align:left;background:#fff}
.scr-table td{padding:9px 10px;border-bottom:1px solid #f8fafc;font-size:0.76rem}
.scr-table tr:hover td{background:#fef9f5;cursor:pointer}

/* ── PORTFOLIO ── */
.pf-card{background:#fff;border:1px solid #f1f5f9;border-radius:8px;padding:10px 14px;margin-bottom:6px}
.pf-sym{font-family:'JetBrains Mono',monospace;font-size:0.75rem;font-weight:600;color:#0f172a}
.pf-meta{font-size:0.65rem;color:#94a3b8;margin-top:2px}
.pf-pnl{font-family:'JetBrains Mono',monospace;font-size:0.8rem;font-weight:600;text-align:right}
.pf-pnl.pos{color:#16a34a}.pf-pnl.neg{color:#dc2626}

/* ── STREAMLIT BUTTON ── */
.stButton>button{
  font-family:'Inter',sans-serif!important;font-size:0.7rem!important;
  font-weight:500!important;border-radius:6px!important;padding:5px 12px!important;
  width:100%!important;background:#f8fafc!important;color:#64748b!important;
  border:1px solid #e2e8f0!important;transition:all 0.12s!important;
}
.stButton>button:hover{background:#f1f5f9!important;color:#1e293b!important;border-color:#cbd5e1!important}
.stButton>button[kind="primary"]{background:#f97316!important;color:#fff!important;border-color:#f97316!important;font-weight:600!important}

/* ── TEXT INPUT ── */
.stTextInput>div>div>input{
  background:#f8fafc!important;border:1px solid #e2e8f0!important;
  color:#1e293b!important;border-radius:6px!important;font-size:0.72rem!important;padding:7px 10px!important;
}
.stTextInput>div>div>input:focus{border-color:#f97316!important;box-shadow:0 0 0 3px #fed7aa22!important;background:#fff!important}
.stTextInput>div>div>input::placeholder{color:#94a3b8!important}
.stTextInput label,[data-testid="stWidgetLabel"]{font-size:0.56rem!important;font-weight:600!important;color:#94a3b8!important;text-transform:uppercase!important;letter-spacing:0.1em!important}

/* ── SELECT ── */
.stSelectbox>div>div{background:#f8fafc!important;border:1px solid #e2e8f0!important;border-radius:6px!important;font-size:0.72rem!important}

/* ── SCTION TITLE ── */
.sct{font-size:0.6rem;font-weight:600;color:#94a3b8;letter-spacing:0.1em;text-transform:uppercase;padding:10px 0 8px;border-bottom:1px solid #f1f5f9;margin-bottom:12px}

/* ── TABS (center content) ── */
.tab-row{display:flex;gap:0;border-bottom:1px solid #f1f5f9;margin-bottom:16px}
.tab-item{font-size:0.72rem;font-weight:500;color:#94a3b8;padding:8px 14px;
  cursor:pointer;border-bottom:2px solid transparent;transition:all 0.12s;white-space:nowrap}
.tab-item:hover{color:#1e293b}
.tab-item.active{color:#f97316;border-bottom:2px solid #f97316;font-weight:600}

[data-testid="stPlotlyChart"]{border-radius:8px;overflow:hidden}
.streamlit-expanderHeader{background:#f8fafc!important;border:1px solid #e2e8f0!important;border-radius:6px!important;font-size:0.68rem!important;color:#64748b!important}
</style>
""", unsafe_allow_html=True)

# ── TICKER TAPE ───────────────────────────────────────────────────────────────
st.markdown('<div class="ticker-wrap">', unsafe_allow_html=True)
components.html(tv_ticker_tape(), height=46, scrolling=False)
st.markdown('</div>', unsafe_allow_html=True)

# ── MAIN LAYOUT ───────────────────────────────────────────────────────────────
sidebar_col, main_col = st.columns([1.8, 8.2])

# ══════════════════════════════════════ SIDEBAR ═══════════════════════════════
with sidebar_col:
    # Logo
    st.markdown("""<div class="sb-logo">
      <div class="sb-logo-icon">D</div>
      <div>
        <div class="sb-logo-text">Dalal</div>
        <div class="sb-logo-sub">MARKET TERMINAL</div>
      </div>
    </div>""", unsafe_allow_html=True)

    # Navigation
    st.markdown('<div class="sb-section">Main Menu</div>', unsafe_allow_html=True)
    for icon, label in NAV_ITEMS:
        is_active = st.session_state.page == label
        cls = "sb-nav-item active" if is_active else "sb-nav-item"
        st.markdown(f'<div class="{cls}"><span class="sb-nav-icon">{icon}</span>{label}</div>',
                    unsafe_allow_html=True)
        if st.button(label, key=f"nav_{label}", use_container_width=True,
                     type="primary" if is_active else "secondary"):
            st.session_state.page = label
            st.rerun()

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

    # Watchlist header
    st.markdown("""<div class="sb-wl-hdr">
      <span class="sb-wl-title">Watchlists</span>
    </div>""", unsafe_allow_html=True)

    # Search to add
    raw_q = st.text_input("", placeholder="Search & add stock…",
                          key="sq", label_visibility="collapsed")
    hits  = do_search(raw_q) if raw_q else []
    if hits:
        for h in hits[:5]:
            ca, cb = st.columns([4,1])
            with ca:
                st.markdown(f'<div style="padding:4px 0 2px 20px;font-size:0.7rem;color:#374151"><b style="color:#f97316">{h["sym"]}</b> — {h["name"][:22]}</div>', unsafe_allow_html=True)
            with cb:
                if st.button("＋", key=f"add_{h['sym']}"):
                    e={"sym":h["sym"]+".NS","name":h["name"],"tv":"NSE:"+h["sym"]}
                    if e not in st.session_state.watchlist:
                        st.session_state.watchlist.append(e)
                    st.rerun()

    # Watchlist items
    to_del = None
    for i, w in enumerate(st.session_state.watchlist):
        q    = qget(w["sym"])
        base = w["sym"].replace(".NS","").replace(".BO","")
        arr, _ = ud(q["pct"]); cls = sc(q["pct"])
        ps   = f"₹{q['p']:,.2f}" if q["p"] else "—"
        pct_ = f"{arr}{abs(q['pct']):.2f}%"
        is_s = w["sym"] == st.session_state.sel

        st.markdown(f"""<div class="wl-chip {'active' if is_s else ''}">
          <div class="wl-dot {cls}"></div>
          <span class="wl-n">{base}</span>
          <span class="wl-p {cls}">{pct_}</span>
        </div>""", unsafe_allow_html=True)

        bc, bd = st.columns([5,1])
        with bc:
            tp = "primary" if is_s else "secondary"
            if st.button(f"{base} {ps}", key=f"ws_{i}", type=tp):
                st.session_state.sel      = w["sym"]
                st.session_state.sel_name = w["name"]
                st.session_state.sel_tv   = w.get("tv","NSE:"+base)
                st.session_state.page     = "Market Data"
                st.rerun()
        with bd:
            if st.button("✕", key=f"wd_{i}"):
                to_del = i

    if to_del is not None:
        st.session_state.watchlist.pop(to_del)
        if st.session_state.watchlist:
            w0 = st.session_state.watchlist[0]
            st.session_state.sel      = w0["sym"]
            st.session_state.sel_name = w0["name"]
            st.session_state.sel_tv   = w0.get("tv","")
        st.rerun()

    # API Keys
    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-section">API Keys</div>', unsafe_allow_html=True)
    nk = st.text_input("", type="password", placeholder="NewsAPI key…",
                       key="nk_inp", label_visibility="collapsed")
    if nk: st.session_state.nkey = nk
    ak = st.text_input("", type="password", placeholder="Anthropic key (AI recap)…",
                       key="ak_inp", label_visibility="collapsed")
    if ak: st.session_state["akey"] = ak


# ══════════════════════════════════════ MAIN ══════════════════════════════════
with main_col:
    page = st.session_state.page

    # ── Page header ──
    page_subtitles = {
        "Dashboard":      "Your market overview at a glance",
        "Market Data":    "Live charts · Indices · OHLC · Fundamentals",
        "Stock Screener": "Filter and discover NSE stocks",
        "Portfolio":      "Track your holdings and P&L",
        "Alerts":         "Price alert management",
        "Settings":       "Preferences and configuration",
    }
    st.markdown(f"""<div class="page-header">
      <div>
        <div class="page-title">{page}</div>
        <div class="page-sub">{page_subtitles.get(page,'')}</div>
      </div>
      <div class="header-time">
        {now_str}
        <div class="live-badge">● LIVE</div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
    PAD = "padding:0 24px"

    # ════════════════════ DASHBOARD ══════════════════════════════════════════
    if page == "Dashboard":
        with st.container():
            st.markdown(f'<div style="{PAD}">', unsafe_allow_html=True)

            # Index summary cards
            ic = st.columns(5)
            for i, idx in enumerate(INDICES):
                q = qget(idx["sym"]); arr, col = ud(q["pct"]); cls = sc(q["pct"])
                with ic[i]:
                    st.markdown(f"""<div class="mc" style="margin-bottom:12px">
                      <div class="mc-l">{idx['name']}</div>
                      <div class="mc-v">{q['p']:,.2f}</div>
                      <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;margin-top:2px;color:{'#16a34a' if q['pct']>=0 else '#dc2626'}">{arr} {abs(q['pct']):.2f}%</div>
                    </div>""", unsafe_allow_html=True)

            # Markets table
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">Markets</div><div class="card-sub">Indian indices, commodities &amp; currencies</div>', unsafe_allow_html=True)
            st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
            st.markdown('<table class="mkt-table"><thead><tr><th>Name</th><th style="text-align:right">Price</th><th style="text-align:right">Change</th><th style="text-align:right">% Change</th><th style="text-align:right">Volume</th></tr></thead><tbody>', unsafe_allow_html=True)
            for m in MARKETS_TABLE:
                q = qget(m["sym"]); arr, _ = ud(q["pct"]); cls = sc(q["pct"])
                ps = f"{q['p']:,.2f}" if q["p"] else "—"
                cs = f"{arr} {abs(q['ch']):,.2f}" if q["ch"] else "—"
                vs = sv(q["vol"], fmt="vol") if q["vol"] else "—"
                st.markdown(f"""<tr>
                  <td><span class="mkt-name">{m['country']} {m['name']}</span></td>
                  <td class="mkt-price">{ps}</td>
                  <td class="mkt-chg {cls}">{cs}</td>
                  <td class="mkt-chg {cls}">{arr} {abs(q['pct']):.2f}%</td>
                  <td class="mkt-vol">{vs}</td>
                </tr>""", unsafe_allow_html=True)
            st.markdown('</tbody></table></div>', unsafe_allow_html=True)

            # Sectors + Daily Recap
            sc2, rc2 = st.columns([1,1])
            with sc2:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="card-title">Sectors</div><div class="card-sub">List of NSE sectors</div>', unsafe_allow_html=True)
                st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
                all_sec = [(s, qget(s["sym"])) for s in SECTORS]
                all_sec.sort(key=lambda x: x[1]["pct"], reverse=True)
                max_abs = max(abs(d["pct"]) for _,d in all_sec) or 1
                for s, d in all_sec:
                    arr, _ = ud(d["pct"]); cls = sc(d["pct"])
                    bw = min(abs(d["pct"]) / max_abs * 100, 100)
                    st.markdown(f"""<div class="sec-row">
                      <span class="sec-name">{s['name']}</span>
                      <span class="sec-pct {cls}">{arr}{abs(d['pct']):.2f}%</span>
                      <div class="sec-bar-wrap"><div class="sec-bar-inner {cls}" style="width:{bw:.0f}%"></div></div>
                    </div>""", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with rc2:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="card-title">Daily Recap</div><div class="card-sub">All new around the world about today\'s market</div>', unsafe_allow_html=True)
                st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

                # AI Summary
                akey = st.session_state.get("akey","")
                if akey:
                    nifty_q = qget("^NSEI"); sensex_q = qget("^BSESN")
                    context = f"NIFTY: {nifty_q['p']:,.0f} ({nifty_q['pct']:+.2f}%), SENSEX: {sensex_q['p']:,.0f} ({sensex_q['pct']:+.2f}%)"
                    summary = ai_summary(akey, context)
                    if summary:
                        st.markdown(f"""<div style="background:#f8fafc;border:1px solid #f1f5f9;border-radius:8px;padding:12px 14px;margin-bottom:12px">
                          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px">
                            <div style="display:flex;align-items:center;gap:8px">
                              <div style="width:28px;height:28px;border-radius:7px;background:#f97316;display:flex;align-items:center;justify-content:center;color:#fff;font-size:0.7rem;font-weight:700">AI</div>
                              <span style="font-size:0.75rem;font-weight:600;color:#0f172a">Market Summary</span>
                            </div>
                            <span style="font-size:0.6rem;color:#94a3b8">Today {now_ist.strftime('%H:%M IST')}</span>
                          </div>
                          <p style="font-size:0.72rem;color:#374151;line-height:1.55">{summary}</p>
                        </div>""", unsafe_allow_html=True)

                arts = news_get(st.session_state.nkey, "India stock market NSE BSE")
                if arts:
                    colors = ["#f97316","#2563eb","#16a34a","#9333ea","#dc2626","#0891b2"]
                    for idx2, a in enumerate(arts[:6]):
                        src   = (a.get("source",{}).get("name",""))[:18]
                        ttl   = (a.get("title",""))[:80]
                        desc  = (a.get("description","") or "")[:120]
                        url   = a.get("url","#")
                        initl = src[0].upper() if src else "N"
                        bg    = colors[idx2 % len(colors)]
                        st.markdown(f"""<div class="news-c" onclick="window.open('{url}','_blank')">
                          <div class="news-logo" style="background:{bg}">{initl}</div>
                          <div class="news-body">
                            <div class="news-src-row">
                              <span class="news-src">{src}</span>
                              <span class="news-time">{tago(a.get('publishedAt',''))}</span>
                            </div>
                            <div class="news-title">{ttl}</div>
                            <div class="news-desc">{desc}</div>
                          </div>
                        </div>""", unsafe_allow_html=True)
                else:
                    st.markdown('<div style="padding:16px 0;font-size:0.72rem;color:#94a3b8;text-align:center">Add NewsAPI key in sidebar for live news</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

    # ════════════════════ MARKET DATA ════════════════════════════════════════
    elif page == "Market Data":
        with st.container():
            st.markdown(f'<div style="{PAD}">', unsafe_allow_html=True)

            q    = qget(st.session_state.sel)
            info = iget(st.session_state.sel)
            arr, col = ud(q["pct"])
            p = q["p"]; ch = q["ch"]; pct = q["pct"]
            hi = q["hi"] or info.get("dayHigh") or 0
            lo = q["lo"] or info.get("dayLow")  or 0
            op_= info.get("open") or info.get("regularMarketOpen") or 0
            pc = q["pc"] or info.get("previousClose") or 0

            # Stock header
            ha, hb = st.columns([3,2])
            with ha:
                st.markdown(f"""<div>
                  <div style="font-size:1.1rem;font-weight:700;color:#0f172a">{st.session_state.sel_name}</div>
                  <div style="font-size:0.62rem;color:#94a3b8;margin-top:2px;font-family:'JetBrains Mono',monospace">{st.session_state.sel} · NSE/BSE · {info.get('sector','')}</div>
                  <div class="ohlc-bar">
                    <div class="otag"><span class="ol">O</span><span class="ov">{'₹'+f'{op_:,.2f}' if op_ else '—'}</span></div>
                    <div class="otag"><span class="ol">H</span><span class="ov-g">{'₹'+f'{hi:,.2f}' if hi else '—'}</span></div>
                    <div class="otag"><span class="ol">L</span><span class="ov-r">{'₹'+f'{lo:,.2f}' if lo else '—'}</span></div>
                    <div class="otag"><span class="ol">PC</span><span class="ov">{'₹'+f'{pc:,.2f}' if pc else '—'}</span></div>
                  </div>
                </div>""", unsafe_allow_html=True)
            with hb:
                st.markdown(f"""<div style="text-align:right">
                  <div style="font-family:'JetBrains Mono',monospace;font-size:2rem;font-weight:700;color:#0f172a;line-height:1">{'₹'+f'{p:,.2f}' if p else '—'}</div>
                  <div style="font-family:'JetBrains Mono',monospace;font-size:0.85rem;font-weight:500;margin-top:4px;color:{col}">{arr} ₹{abs(ch):,.2f} ({abs(pct):.2f}%)</div>
                </div>""", unsafe_allow_html=True)

            st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)

            # TradingView chart
            st.markdown('<div class="card" style="padding:0;overflow:hidden">', unsafe_allow_html=True)
            components.html(tv_chart(st.session_state.sel_tv, height=520, interval="D"), height=520)
            st.markdown('</div>', unsafe_allow_html=True)

            # Detail tabs
            DTABS = ["Overview","Fundamentals","Financials","News"]
            if "dtab" not in st.session_state: st.session_state.dtab = "Overview"
            tcols = st.columns(len(DTABS))
            for i, t in enumerate(DTABS):
                tp = "primary" if st.session_state.dtab == t else "secondary"
                if tcols[i].button(t, key=f"dt_{t}", type=tp):
                    st.session_state.dtab = t; st.rerun()

            dtab = st.session_state.dtab

            if dtab == "Overview":
                mcap=info.get("marketCap"); wh52=info.get("fiftyTwoWeekHigh")
                wl52=info.get("fiftyTwoWeekLow"); pe_=info.get("trailingPE")
                fpe=info.get("forwardPE"); eps=info.get("trailingEps")
                dy=info.get("dividendYield"); vol=info.get("volume") or info.get("regularMarketVolume")
                avol=info.get("averageVolume"); beta=info.get("beta"); ptb=info.get("priceToBook")
                wk52pct = round((p-wl52)/(wh52-wl52)*100,1) if (wh52 and wl52 and p and wh52!=wl52) else None
                metrics=[
                    ("Market Cap",finr(mcap),""),("52W High",sv(wh52),""),("52W Low",sv(wl52),""),
                    ("52W Range",f"{wk52pct:.0f}%" if wk52pct is not None else "—",""),
                    ("P/E (TTM)",sv(pe_,"",dec=1),""),("Fwd P/E",sv(fpe,"",dec=1),""),
                    ("EPS (TTM)",sv(eps),""),("Div Yield",sv(dy,fmt="pct"),"pos" if dy and float(dy or 0)>0 else ""),
                    ("Volume",sv(vol,fmt="vol"),""),("Avg Volume",sv(avol,fmt="vol"),""),
                    ("Beta",sv(beta,"",dec=2),""),("Price/Book",sv(ptb,"",dec=2),""),
                ]
                mc4=st.columns(4)
                for idx_,(lbl,val,vc) in enumerate(metrics):
                    mvc=f"mc-v {vc}".strip()
                    with mc4[idx_%4]:
                        st.markdown(f'<div class="mc" style="margin-bottom:8px"><div class="mc-l">{lbl}</div><div class="{mvc}">{val}</div></div>', unsafe_allow_html=True)

            elif dtab == "Fundamentals":
                roe=info.get("returnOnEquity"); roa=info.get("returnOnAssets")
                gm=info.get("grossMargins"); om=info.get("operatingMargins")
                pm=info.get("profitMargins"); d2e=info.get("debtToEquity")
                cr=info.get("currentRatio"); fcf=info.get("freeCashflow")
                rev=info.get("totalRevenue"); ebit=info.get("ebitda")
                ni=info.get("netIncomeToCommon"); eg=info.get("earningsGrowth")
                rg=info.get("revenueGrowth"); bv=info.get("bookValue")
                td=info.get("totalDebt"); tc_=info.get("totalCash")
                evr=info.get("enterpriseToRevenue"); eve=info.get("enterpriseToEbitda")
                f1,f2,f3=st.columns(3)
                def tbl(rows):
                    s='<table class="ft">'
                    for l,v in rows: s+=f'<tr><td class="fl">{l}</td><td class="fv">{v}</td></tr>'
                    return s+'</table>'
                with f1:
                    st.markdown('<div class="sct">Income</div>', unsafe_allow_html=True)
                    st.markdown(tbl([("Revenue",finr(rev)),("EBITDA",finr(ebit)),
                        ("Net Income",finr(ni)),("Free Cash Flow",finr(fcf)),
                        ("Gross Margin",sv(gm,fmt="pct")),("Op Margin",sv(om,fmt="pct")),
                        ("Net Margin",sv(pm,fmt="pct")),("ROE",sv(roe,fmt="pct")),
                        ("ROA",sv(roa,fmt="pct"))]), unsafe_allow_html=True)
                with f2:
                    st.markdown('<div class="sct">Balance Sheet</div>', unsafe_allow_html=True)
                    nd_=finr(float(td)-float(tc_)) if (td and tc_) else "—"
                    st.markdown(tbl([("Total Debt",finr(td)),("Total Cash",finr(tc_)),
                        ("Net Debt",nd_),("Debt/Equity",sv(d2e,"",dec=2)),
                        ("Current Ratio",sv(cr,"",dec=2)),("Book Value/Sh",sv(bv,dec=2)),
                        ("Shares Out",sv(info.get("sharesOutstanding"),fmt="vol"))]),unsafe_allow_html=True)
                with f3:
                    st.markdown('<div class="sct">Valuation &amp; Growth</div>', unsafe_allow_html=True)
                    st.markdown(tbl([("EV/Revenue",sv(evr,"",dec=2)),("EV/EBITDA",sv(eve,"",dec=2)),
                        ("Rev Growth",sv(rg,fmt="pct")),("Earn Growth",sv(eg,fmt="pct")),
                        ("Earn Gr QoQ",sv(info.get("earningsQuarterlyGrowth"),fmt="pct")),
                        ("Sector",info.get("sector","—")),("Industry",info.get("industry","—"))]),unsafe_allow_html=True)
                summary=info.get("longBusinessSummary","")
                if summary:
                    st.markdown(f'<div style="font-size:0.7rem;color:#64748b;line-height:1.65;margin-top:10px;padding:12px 14px;background:#f8fafc;border:1px solid #f1f5f9;border-radius:7px">{summary[:800]}…</div>',unsafe_allow_html=True)

            elif dtab == "Financials":
                try:
                    t_obj=yf.Ticker(st.session_state.sel)
                    fin=t_obj.financials; bs=t_obj.balance_sheet; cf=t_obj.cashflow
                    def rdf(df_in,label):
                        if df_in is None or df_in.empty:
                            st.markdown(f'<div style="padding:8px;color:#94a3b8;font-size:0.65rem">{label}: not available</div>',unsafe_allow_html=True); return
                        st.markdown(f'<div class="sct">{label}</div>',unsafe_allow_html=True)
                        d=df_in.head(8).copy()
                        d.index=[str(x)[:35] for x in d.index]
                        d.columns=[str(c)[:11] for c in d.columns]
                        def fc(x):
                            try:
                                f=float(x)
                                if abs(f)>=1e7: return f"₹{f/1e7:.1f}Cr"
                                if abs(f)>=1e5: return f"₹{f/1e5:.1f}L"
                                return f"₹{f:,.0f}"
                            except: return "—"
                        st.dataframe(d.map(fc),use_container_width=True)
                    rdf(fin,"Income Statement"); rdf(bs,"Balance Sheet"); rdf(cf,"Cash Flow")
                except Exception as e:
                    st.markdown(f'<div style="padding:10px;color:#94a3b8;font-size:0.68rem">Could not load financials.</div>',unsafe_allow_html=True)

            elif dtab == "News":
                arts = news_get(st.session_state.nkey, f"India {st.session_state.sel_name} NSE stock")
                if arts:
                    colors2=["#f97316","#2563eb","#16a34a","#9333ea","#dc2626","#0891b2"]
                    for idx2,a in enumerate(arts[:15]):
                        src=(a.get("source",{}).get("name",""))[:20]
                        ttl=(a.get("title",""))[:90]
                        desc=(a.get("description","") or "")[:130]
                        url=a.get("url","#")
                        initl=src[0].upper() if src else "N"
                        bg=colors2[idx2%len(colors2)]
                        st.markdown(f"""<div class="news-c" onclick="window.open('{url}','_blank')">
                          <div class="news-logo" style="background:{bg}">{initl}</div>
                          <div class="news-body">
                            <div class="news-src-row"><span class="news-src">{src}</span><span class="news-time">{tago(a.get('publishedAt',''))}</span></div>
                            <div class="news-title">{ttl}</div>
                            <div class="news-desc">{desc}</div>
                          </div>
                        </div>""",unsafe_allow_html=True)
                else:
                    st.markdown('<div style="padding:20px 0;text-align:center;color:#94a3b8;font-size:0.72rem">Add NewsAPI key in sidebar for news</div>',unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

    # ════════════════════ STOCK SCREENER ════════════════════════════════════
    elif page == "Stock Screener":
        st.markdown(f'<div style="{PAD}">', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">NSE Stock Screener</div><div class="card-sub">Filter stocks by sector, performance and metrics</div><div style="height:10px"></div>', unsafe_allow_html=True)

        fa, fb, fc2, fd = st.columns(4)
        with fa:
            sort_by = st.selectbox("Sort by", ["% Change","Price","Market Cap"], label_visibility="visible")
        with fb:
            direction = st.selectbox("Direction", ["Top Gainers","Top Losers","All"], label_visibility="visible")
        with fc2:
            screen_n = st.selectbox("Show", [10,20,30,50], label_visibility="visible")

        rows_scr=[]
        for sym in NIFTY50:
            qr=qget(sym); base=sym.replace(".NS","")
            rows_scr.append({"sym":base,"full":sym,"name":NSE_STOCKS.get(base,base),
                             "p":qr["p"],"pct":qr["pct"],"ch":qr["ch"],"vol":qr["vol"]})

        if direction=="Top Gainers": rows_scr.sort(key=lambda x:x["pct"],reverse=True)
        elif direction=="Top Losers": rows_scr.sort(key=lambda x:x["pct"])
        else:
            if sort_by=="Price": rows_scr.sort(key=lambda x:x["p"],reverse=True)
            elif sort_by=="% Change": rows_scr.sort(key=lambda x:abs(x["pct"]),reverse=True)

        st.markdown('<table class="scr-table"><thead><tr><th>Symbol</th><th>Company</th><th style="text-align:right">Price</th><th style="text-align:right">Change</th><th style="text-align:right">% Change</th><th style="text-align:right">Volume</th></tr></thead><tbody>',unsafe_allow_html=True)
        for r in rows_scr[:int(screen_n)]:
            arr_r,_=ud(r["pct"]); cls_r=sc(r["pct"])
            ps=f"₹{r['p']:,.2f}" if r["p"] else "—"
            cs=f"{arr_r} ₹{abs(r['ch']):,.2f}" if r["ch"] else "—"
            vs=sv(r["vol"],fmt="vol") if r["vol"] else "—"
            pcts=f'<span style="color:{"#16a34a" if r["pct"]>=0 else "#dc2626"};font-family:JetBrains Mono,monospace;font-weight:600">{arr_r}{abs(r["pct"]):.2f}%</span>'
            st.markdown(f"""<tr>
              <td style="font-family:'JetBrains Mono',monospace;font-weight:600;color:#f97316">{r['sym']}</td>
              <td style="color:#374151">{r['name'][:28]}</td>
              <td style="font-family:'JetBrains Mono',monospace;text-align:right;font-weight:500">{ps}</td>
              <td style="font-family:'JetBrains Mono',monospace;text-align:right;color:{'#16a34a' if r['pct']>=0 else '#dc2626'}">{cs}</td>
              <td style="text-align:right">{pcts}</td>
              <td style="font-family:'JetBrains Mono',monospace;text-align:right;color:#64748b">{vs}</td>
            </tr>""",unsafe_allow_html=True)
        st.markdown('</tbody></table></div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)

    # ════════════════════ PORTFOLIO ══════════════════════════════════════════
    elif page == "Portfolio":
        st.markdown(f'<div style="{PAD}">', unsafe_allow_html=True)
        pa, pb = st.columns([3,2])
        with pa:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">Add Position</div><div style="height:8px"></div>', unsafe_allow_html=True)
            p1,p2,p3=st.columns(3)
            with p1: pt_sym=st.text_input("Ticker",placeholder="RELIANCE",label_visibility="visible",key="pt_sym")
            with p2: pt_qty=st.text_input("Quantity",placeholder="10",label_visibility="visible",key="pt_qty")
            with p3: pt_buy=st.text_input("Buy Price ₹",placeholder="2800",label_visibility="visible",key="pt_buy")
            if st.button("Add to Portfolio",type="primary"):
                if pt_sym and pt_qty and pt_buy:
                    try:
                        sym=to_sym(pt_sym)
                        base=pt_sym.strip().upper().replace(".NS","")
                        st.session_state.portfolio.append({
                            "sym":sym,"base":base,"name":NSE_STOCKS.get(base,base),
                            "qty":float(pt_qty),"buy":float(pt_buy)
                        })
                        st.rerun()
                    except: pass
            st.markdown('</div>',unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">Holdings</div><div style="height:8px"></div>',unsafe_allow_html=True)
            if st.session_state.portfolio:
                total_val=0; total_cost=0
                del_idx=None
                for i,pos in enumerate(st.session_state.portfolio):
                    q_=qget(pos["sym"])
                    curr_val=q_["p"]*pos["qty"]; cost=pos["buy"]*pos["qty"]
                    pnl=curr_val-cost; pnl_pct=(pnl/cost*100) if cost else 0
                    total_val+=curr_val; total_cost+=cost
                    arr_,_=ud(pnl_pct); cls_=sc(pnl_pct)
                    pa2,pb2=st.columns([5,1])
                    with pa2:
                        st.markdown(f"""<div class="pf-card">
                          <div style="display:flex;justify-content:space-between;align-items:flex-start">
                            <div>
                              <div class="pf-sym">{pos['base']}</div>
                              <div class="pf-meta">{pos['name'][:28]} · {pos['qty']:.0f} @ ₹{pos['buy']:,.2f}</div>
                            </div>
                            <div>
                              <div class="pf-pnl {cls_}">₹{pnl:,.0f}</div>
                              <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;text-align:right;color:{'#16a34a' if pnl>=0 else '#dc2626'}">{arr_}{abs(pnl_pct):.2f}%</div>
                            </div>
                          </div>
                        </div>""",unsafe_allow_html=True)
                    with pb2:
                        if st.button("✕",key=f"del_pos_{i}"): del_idx=i
                if del_idx is not None:
                    st.session_state.portfolio.pop(del_idx); st.rerun()
                total_pnl=total_val-total_cost
                arr_t,_=ud(total_pnl)
                st.markdown(f"""<div style="background:#f8fafc;border:1px solid #f1f5f9;border-radius:8px;padding:12px 14px;margin-top:8px">
                  <div style="display:flex;justify-content:space-between">
                    <span style="font-size:0.72rem;font-weight:600;color:#64748b">TOTAL P&amp;L</span>
                    <span style="font-family:'JetBrains Mono',monospace;font-size:0.9rem;font-weight:700;color:{'#16a34a' if total_pnl>=0 else '#dc2626'}">{arr_t} ₹{abs(total_pnl):,.0f}</span>
                  </div>
                  <div style="display:flex;justify-content:space-between;margin-top:4px">
                    <span style="font-size:0.68rem;color:#94a3b8">Portfolio Value</span>
                    <span style="font-family:'JetBrains Mono',monospace;font-size:0.75rem;font-weight:600;color:#1e293b">₹{total_val:,.0f}</span>
                  </div>
                </div>""",unsafe_allow_html=True)
            else:
                st.markdown('<div style="padding:20px 0;text-align:center;color:#94a3b8;font-size:0.72rem">No positions yet. Add your first holding above.</div>',unsafe_allow_html=True)
            st.markdown('</div>',unsafe_allow_html=True)

        with pb:
            if st.session_state.portfolio:
                st.markdown('<div class="card" style="padding:0;overflow:hidden">', unsafe_allow_html=True)
                components.html(tv_chart(st.session_state.sel_tv, height=400), height=400)
                st.markdown('</div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)

    # ════════════════════ ALERTS ════════════════════════════════════════════
    elif page == "Alerts":
        st.markdown(f'<div style="{PAD}">', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Price Alerts</div><div class="card-sub">Get notified when a stock hits your target price</div><div style="height:10px"></div>',unsafe_allow_html=True)
        a1,a2,a3=st.columns(3)
        with a1: al_sym=st.text_input("Stock",placeholder="RELIANCE",key="al_sym",label_visibility="visible")
        with a2: al_price=st.text_input("Target Price ₹",placeholder="1500",key="al_price",label_visibility="visible")
        with a3: al_type=st.selectbox("Alert Type",["Above","Below"],label_visibility="visible")
        if st.button("Set Alert",type="primary"):
            if al_sym and al_price:
                if "alerts" not in st.session_state: st.session_state.alerts=[]
                sym=to_sym(al_sym)
                q_=qget(sym)
                triggered=False
                if al_type=="Above" and q_["p"]>float(al_price): triggered=True
                if al_type=="Below" and q_["p"]<float(al_price): triggered=True
                st.session_state.alerts.append({"sym":al_sym.upper(),"price":float(al_price),"type":al_type,"triggered":triggered,"set_at":now_ist.strftime("%H:%M IST")})
                st.rerun()

        if "alerts" in st.session_state and st.session_state.alerts:
            st.markdown('<div style="height:12px"></div>',unsafe_allow_html=True)
            del_a=None
            for i,al in enumerate(st.session_state.alerts):
                q_=qget(to_sym(al["sym"]))
                status_c="#16a34a" if al["triggered"] else "#f59e0b"
                status_t="Triggered" if al["triggered"] else "Watching"
                aa,ab=st.columns([5,1])
                with aa:
                    st.markdown(f"""<div style="background:#f8fafc;border:1px solid #f1f5f9;border-radius:7px;padding:10px 14px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center">
                      <div>
                        <span style="font-family:'JetBrains Mono',monospace;font-weight:600;color:#0f172a">{al['sym']}</span>
                        <span style="font-size:0.68rem;color:#64748b;margin-left:8px">{al['type']} ₹{al['price']:,.2f}</span>
                      </div>
                      <div style="display:flex;align-items:center;gap:10px">
                        <span style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:#94a3b8">Now: ₹{q_['p']:,.2f}</span>
                        <span style="font-size:0.62rem;color:{status_c};background:{status_c}22;padding:2px 8px;border-radius:20px;font-weight:500">{status_t}</span>
                      </div>
                    </div>""",unsafe_allow_html=True)
                with ab:
                    if st.button("✕",key=f"del_al_{i}"): del_a=i
            if del_a is not None:
                st.session_state.alerts.pop(del_a); st.rerun()
        else:
            st.markdown('<div style="padding:16px 0;text-align:center;color:#94a3b8;font-size:0.72rem">No alerts set yet.</div>',unsafe_allow_html=True)
        st.markdown('</div></div>',unsafe_allow_html=True)

    # ════════════════════ SETTINGS ══════════════════════════════════════════
    elif page == "Settings":
        st.markdown(f'<div style="{PAD}">', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">About Dalal Terminal</div><div style="height:8px"></div>',unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size:0.75rem;color:#374151;line-height:1.8">
          <b>Data Source:</b> Yahoo Finance via yfinance (free, ~15 min delayed)<br>
          <b>Charts:</b> TradingView embedded widgets (real-time)<br>
          <b>News:</b> NewsAPI.org (free tier: 100 req/day)<br>
          <b>AI Recap:</b> Claude API (Anthropic) — optional<br><br>
          <b>Symbol Format:</b> NSE stocks use <code>SYMBOL.NS</code> · BSE use <code>SYMBOL.BO</code><br>
          <b>TradingView Format:</b> <code>NSE:SYMBOL</code> · e.g. <code>NSE:RELIANCE</code>
        </div>
        """,unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)

        if st.button("⟳  Clear Cache & Refresh All Data",type="primary"):
            st.cache_data.clear(); st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)

    # ════════════════════ FALLBACK ══════════════════════════════════════════
    else:
        st.markdown(f'<div style="{PAD}"><div class="card"><div class="card-title">{page}</div><div style="padding:20px 0;color:#94a3b8;font-size:0.75rem">Coming soon.</div></div></div>',unsafe_allow_html=True)
