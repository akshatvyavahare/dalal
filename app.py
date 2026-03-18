import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timezone, timedelta
import requests

st.set_page_config(page_title="Dalal Terminal", page_icon="◈",
                   layout="wide", initial_sidebar_state="collapsed")

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
    "LTTS":"L&T Tech Services","NH":"Narayana Hrudayalaya","NLCINDIA":"NLC India",
    "OLECTRA":"Olectra Greentech","PVR":"PVR INOX","RBLBANK":"RBL Bank",
    "RITES":"RITES","SCHAEFFLER":"Schaeffler India","SOBHA":"Sobha",
    "STARHEALTH":"Star Health","SUNDARMFIN":"Sundaram Finance",
    "SUPREMEIND":"Supreme Industries","TANLA":"Tanla Platforms",
    "THERMAX":"Thermax","TIINDIA":"Tube Investments","TRIDENT":"Trident",
    "VINATIORGA":"Vinati Organics","ZEEL":"Zee Entertainment",
    "ZYDUSLIFE":"Zydus Lifesciences","KPITTECH":"KPIT Technologies",
    "KAYNES":"Kaynes Technology","MAPMYINDIA":"MapmyIndia","CAMPUS":"Campus Activewear",
}
INDICES=[
    {"sym":"^NSEI","name":"NIFTY 50"},{"sym":"^BSESN","name":"SENSEX"},
    {"sym":"^NSMIDCP","name":"NIFTY MID"},{"sym":"^CNXIT","name":"NIFTY IT"},
    {"sym":"^CNXBANK","name":"BANK NIFTY"},
]
COMMODITIES=[
    {"sym":"GC=F","name":"Gold"},{"sym":"SI=F","name":"Silver"},
    {"sym":"CL=F","name":"Crude Oil"},{"sym":"NG=F","name":"Nat Gas"},
    {"sym":"USDINR=X","name":"USD/INR"},{"sym":"EURINR=X","name":"EUR/INR"},
    {"sym":"GBPINR=X","name":"GBP/INR"},
]
MCX_LIST=[
    {"sym":"TATASTEEL.NS","name":"Tata Steel"},{"sym":"HINDALCO.NS","name":"Hindalco"},
    {"sym":"JSWSTEEL.NS","name":"JSW Steel"},{"sym":"VEDL.NS","name":"Vedanta"},
    {"sym":"NMDC.NS","name":"NMDC"},{"sym":"SAIL.NS","name":"SAIL"},
    {"sym":"HINDZINC.NS","name":"Hind Zinc"},{"sym":"ONGC.NS","name":"ONGC"},
    {"sym":"BPCL.NS","name":"BPCL"},{"sym":"IOC.NS","name":"Indian Oil"},
    {"sym":"GAIL.NS","name":"GAIL"},{"sym":"MCX.NS","name":"MCX India"},
]
SECTORS=[
    {"sym":"^CNXIT","name":"IT"},{"sym":"^CNXBANK","name":"Banking"},
    {"sym":"^CNXPHARMA","name":"Pharma"},{"sym":"^CNXFMCG","name":"FMCG"},
    {"sym":"^CNXAUTO","name":"Auto"},{"sym":"^CNXREALTY","name":"Realty"},
    {"sym":"^CNXMETAL","name":"Metal"},{"sym":"^CNXENERGY","name":"Energy"},
]
ALL_IDX=[
    {"sym":"^NSEI","name":"NIFTY 50"},{"sym":"^BSESN","name":"SENSEX"},
    {"sym":"^NSMIDCP","name":"NIFTY Midcap"},{"sym":"^CNXSMALLCAP","name":"NIFTY Smallcap"},
    {"sym":"^CNXBANK","name":"Bank NIFTY"},{"sym":"^CNXIT","name":"NIFTY IT"},
    {"sym":"^CNXPHARMA","name":"NIFTY Pharma"},{"sym":"^CNXFMCG","name":"NIFTY FMCG"},
    {"sym":"^CNXAUTO","name":"NIFTY Auto"},{"sym":"^CNXREALTY","name":"NIFTY Realty"},
    {"sym":"^CNXMETAL","name":"NIFTY Metal"},{"sym":"^CNXENERGY","name":"NIFTY Energy"},
    {"sym":"^CNXINFRA","name":"NIFTY Infra"},{"sym":"^CNXPSUBANK","name":"NIFTY PSU Bank"},
    {"sym":"^CNXPRIVATEBANK","name":"NIFTY Pvt Bank"},
]
NIFTY50=[k+".NS" for k in [
    "RELIANCE","TCS","HDFCBANK","INFY","ICICIBANK","HINDUNILVR","ITC","SBIN",
    "BHARTIARTL","KOTAKBANK","LT","AXISBANK","ASIANPAINT","MARUTI","TITAN",
    "WIPRO","BAJFINANCE","NESTLEIND","ULTRACEMCO","TECHM","SUNPHARMA","HCLTECH",
    "POWERGRID","NTPC","TATAMOTORS","HINDALCO","JSWSTEEL","ONGC","BPCL",
    "COALINDIA","GRASIM","ADANIENT","ADANIPORTS","TATASTEEL","BAJAJFINSV",
    "BAJAJ-AUTO","DIVISLAB","DRREDDY","EICHERMOT","HEROMOTOCO","INDUSINDBK",
    "M&M","TATACONSUM","TATAPOWER","TRENT","UPL","VEDL","BRITANNIA","CIPLA","LUPIN",
]]
PERIODS={"1D":("1d","5m"),"1W":("5d","15m"),"1M":("1mo","1h"),
          "3M":("3mo","1d"),"6M":("6mo","1d"),"1Y":("1y","1d"),"3Y":("3y","1wk")}
IST=timezone(timedelta(hours=5,minutes=30))

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
ss("ctab","Overview"); ss("nkey",""); ss("add_input","")

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

def do_search(q):
    q=q.strip().upper()
    if len(q)<2: return []
    return [{"sym":k,"name":v} for k,v in NSE_STOCKS.items()
            if q in k or q in v.upper()][:6]

def calc_technicals(df):
    if df.empty or "Close" not in df.columns: return {}
    c=df["Close"].astype(float); t={}
    if len(c)>=20:  t["MA20"]=round(float(c.rolling(20).mean().iloc[-1]),2)
    if len(c)>=50:  t["MA50"]=round(float(c.rolling(50).mean().iloc[-1]),2)
    if len(c)>=200: t["MA200"]=round(float(c.rolling(200).mean().iloc[-1]),2)
    if len(c)>=15:
        delta=c.diff(); gain=delta.clip(lower=0).rolling(14).mean()
        loss=(-delta.clip(upper=0)).rolling(14).mean()
        rs=gain/loss.replace(0,float("nan"))
        t["RSI14"]=round(float((100-(100/(1+rs))).iloc[-1]),1)
    if len(c)>=26:
        e12=c.ewm(span=12,adjust=False).mean(); e26=c.ewm(span=26,adjust=False).mean()
        macd=e12-e26; sig=macd.ewm(span=9,adjust=False).mean()
        t["MACD"]=round(float(macd.iloc[-1]),2)
        t["MACD_Signal"]=round(float(sig.iloc[-1]),2)
        t["MACD_Hist"]=round(float((macd-sig).iloc[-1]),2)
    if len(c)>=20:
        ma=c.rolling(20).mean(); sd=c.rolling(20).std()
        t["BB_Upper"]=round(float((ma+2*sd).iloc[-1]),2)
        t["BB_Lower"]=round(float((ma-2*sd).iloc[-1]),2)
    if len(c)>=20:
        t["Volatility_Ann%"]=round(float(c.pct_change().dropna().std()*(252**0.5)*100),1)
    cur=float(c.iloc[-1]); t["Current"]=cur
    t["1M_%"]=round((cur/float(c.iloc[-min(22,len(c))])-1)*100,2)
    t["3M_%"]=round((cur/float(c.iloc[-min(66,len(c))])-1)*100,2)
    t["6M_%"]=round((cur/float(c.iloc[-min(130,len(c))])-1)*100,2)
    if "Volume" in df.columns:
        v=df["Volume"].astype(float)
        if len(v)>=20: t["Vol_Ratio_10d"]=round(float(v.iloc[-5:].mean()/v.iloc[-20:].mean()),2)
    return t

def call_claude(prompt:str)->str:
    try:
        resp=requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={"Content-Type":"application/json"},
            json={"model":"claude-sonnet-4-20250514","max_tokens":1500,
                  "messages":[{"role":"user","content":prompt}]},
            timeout=90,
        )
        data=resp.json()
        return "".join(b.get("text","") for b in data.get("content",[]) if b.get("type")=="text")
    except Exception as e:
        return f"Error calling AI: {e}"

now_ist=datetime.now(IST)
now_str=now_ist.strftime("%d %b %Y  %H:%M IST")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap');
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body,[class*="css"]{font-family:'Inter',sans-serif;background:#f0f2f5!important;color:#1e293b}
.main .block-container{padding:0!important;max-width:100%!important}
section[data-testid="stSidebar"]{display:none!important}
#MainMenu,footer,header,[data-testid="stToolbar"],.stDeployButton{display:none!important}
::-webkit-scrollbar{width:4px;background:transparent}
::-webkit-scrollbar-thumb{background:#cbd5e1;border-radius:4px}

/* TOPBAR */
.topbar{display:flex;align-items:center;gap:8px;padding:0 18px;height:50px;
  background:#fff;border-bottom:1px solid #e2e8f0;
  position:sticky;top:0;z-index:200;box-shadow:0 1px 3px rgba(0,0,0,0.06);overflow-x:auto}
.t-logo{font-family:'JetBrains Mono',monospace;font-size:0.8rem;font-weight:600;
  color:#0f172a;letter-spacing:0.14em;white-space:nowrap;display:flex;align-items:center;gap:5px;margin-right:10px}
.t-dot{color:#f97316}
.ic{display:flex;flex-direction:column;justify-content:center;padding:4px 10px;
  border-radius:5px;background:#f8fafc;border:1px solid #e2e8f0;min-width:86px;white-space:nowrap}
.ic-n{font-size:0.51rem;color:#94a3b8;letter-spacing:0.08em;text-transform:uppercase;font-family:'JetBrains Mono',monospace}
.ic-v{font-family:'JetBrains Mono',monospace;font-size:0.76rem;font-weight:600;color:#0f172a;line-height:1.3}
.ic-c{font-family:'JetBrains Mono',monospace;font-size:0.58rem;font-weight:500}
.ic-c.pos{color:#16a34a}.ic-c.neg{color:#dc2626}
.t-r{margin-left:auto;display:flex;align-items:center;gap:10px;flex-shrink:0}
.t-time{font-family:'JetBrains Mono',monospace;font-size:0.58rem;color:#94a3b8;white-space:nowrap}
.t-live{font-size:0.58rem;color:#16a34a;background:#f0fdf4;border:1px solid #bbf7d0;
  padding:2px 8px;border-radius:20px;font-weight:500;font-family:'JetBrains Mono',monospace}

/* COLUMN PANELS — target Streamlit nth column */
[data-testid="column"]{padding:0!important}
[data-testid="column"]:nth-of-type(1)>div:first-child{
  background:#fff;border-right:1px solid #e2e8f0;
  height:calc(100vh - 50px);overflow-y:auto;overflow-x:hidden}
[data-testid="column"]:nth-of-type(2)>div:first-child{
  background:#f0f2f5;height:calc(100vh - 50px);overflow-y:auto;padding:14px 16px}
[data-testid="column"]:nth-of-type(3)>div:first-child{
  background:#fff;border-left:1px solid #e2e8f0;
  height:calc(100vh - 50px);overflow-y:auto;overflow-x:hidden}

/* PANEL SECTION HEADER */
.sh{font-size:0.57rem;font-weight:600;color:#94a3b8;letter-spacing:0.12em;
  text-transform:uppercase;padding:9px 13px 7px;border-bottom:1px solid #f1f5f9}

/* SEARCH BOX */
.stTextInput>div>div>input{
  background:#f8fafc!important;border:1px solid #e2e8f0!important;
  color:#1e293b!important;border-radius:6px!important;
  font-size:0.72rem!important;padding:7px 10px!important;font-family:'Inter',sans-serif!important}
.stTextInput>div>div>input:focus{border-color:#f97316!important;box-shadow:0 0 0 3px #fed7aa33!important;background:#fff!important}
.stTextInput>div>div>input::placeholder{color:#94a3b8!important}
.stTextInput label,[data-testid="stWidgetLabel"]{font-size:0!important;height:0!important;display:none!important}

/* SEARCH DROPDOWN */
.sr-drop{background:#fff;border:1px solid #e2e8f0;border-radius:6px;
  margin:2px 10px 6px;box-shadow:0 4px 14px rgba(0,0,0,0.09);overflow:hidden}
.sr-row{padding:7px 10px;border-bottom:1px solid #f8fafc;cursor:pointer;transition:background 0.1s}
.sr-row:last-child{border-bottom:none}
.sr-row:hover{background:#fef9f5}
.sr-sym{font-family:'JetBrains Mono',monospace;font-size:0.7rem;font-weight:600;color:#f97316}
.sr-nm{font-size:0.6rem;color:#64748b;margin-top:1px}

/* WATCHLIST */
.wl-item{display:flex;align-items:center;padding:8px 12px;
  border-bottom:1px solid #f8fafc;transition:background 0.1s;gap:8px}
.wl-item:hover{background:#fef9f5;cursor:pointer}
.wl-item.wl-sel{background:#fff7ed;border-left:3px solid #f97316}
.wl-sym{font-family:'JetBrains Mono',monospace;font-size:0.7rem;font-weight:600;color:#1e293b;min-width:60px}
.wl-price{font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:#374151;flex:1}
.wl-pct{font-size:0.62rem;font-weight:500;padding:1px 5px;border-radius:3px}
.wl-pct.pos{color:#16a34a;background:#f0fdf4}.wl-pct.neg{color:#dc2626;background:#fef2f2}

/* BUTTONS */
.stButton>button{
  font-family:'Inter',sans-serif!important;font-size:0.68rem!important;
  font-weight:500!important;border-radius:5px!important;padding:4px 8px!important;
  width:100%!important;background:transparent!important;color:#94a3b8!important;
  border:1px solid #f1f5f9!important;transition:all 0.12s!important;
  margin:0!important;line-height:1.4!important}
.stButton>button:hover{background:#fef9f5!important;color:#f97316!important;border-color:#fed7aa!important}
.stButton>button[kind="primary"]{background:#f97316!important;color:#fff!important;border-color:#f97316!important;font-weight:600!important}

/* NEWS */
.ni{padding:8px 13px;border-bottom:1px solid #f8fafc;cursor:pointer;transition:background 0.1s}
.ni:hover{background:#f8fafc}
.ni-s{font-size:0.55rem;font-weight:600;color:#f97316;text-transform:uppercase;letter-spacing:0.06em}
.ni-t{font-size:0.67rem;color:#334155;line-height:1.4;margin-top:2px}
.ni-d{font-size:0.55rem;color:#94a3b8;margin-top:2px;font-family:'JetBrains Mono',monospace}

/* STOCK BANNER */
.banner{background:#fff;border-radius:9px;padding:13px 16px;border:1px solid #e2e8f0;
  margin-bottom:11px;box-shadow:0 1px 4px rgba(0,0,0,0.05)}
.bn-name{font-size:0.95rem;font-weight:600;color:#0f172a}
.bn-sub{font-size:0.58rem;color:#94a3b8;margin-top:2px;font-family:'JetBrains Mono',monospace}
.bn-price{font-family:'JetBrains Mono',monospace;font-size:1.75rem;font-weight:600;
  color:#0f172a;line-height:1;text-align:right}
.bn-chg{font-family:'JetBrains Mono',monospace;font-size:0.76rem;font-weight:500;
  text-align:right;margin-top:4px}
.orow{display:flex;gap:5px;flex-wrap:wrap;margin-top:9px}
.otag{background:#f8fafc;border:1px solid #e2e8f0;border-radius:4px;
  padding:2px 9px;font-family:'JetBrains Mono',monospace;font-size:0.61rem}
.ol{color:#94a3b8;margin-right:2px}
.ov{color:#1e293b;font-weight:600}.ov-g{color:#16a34a;font-weight:600}.ov-r{color:#dc2626;font-weight:600}

/* CHART WRAP */
.chart-wrap{background:#fff;border:1px solid #e2e8f0;border-radius:9px;
  padding:10px 10px 4px;margin-bottom:11px;box-shadow:0 1px 4px rgba(0,0,0,0.05)}

/* SECTION TITLE */
.sct{font-size:0.58rem;font-weight:600;color:#94a3b8;letter-spacing:0.1em;
  text-transform:uppercase;padding:9px 0 7px;border-bottom:1px solid #f1f5f9;margin-bottom:10px}

/* METRIC CARDS */
.mc{background:#fff;border:1px solid #e2e8f0;border-radius:7px;
  padding:9px 11px;box-shadow:0 1px 3px rgba(0,0,0,0.04)}
.mc-l{font-size:0.53rem;font-weight:500;color:#94a3b8;text-transform:uppercase;letter-spacing:0.08em}
.mc-v{font-family:'JetBrains Mono',monospace;font-size:0.8rem;font-weight:600;color:#1e293b;margin-top:4px}
.mc-v.pos{color:#16a34a}.mc-v.neg{color:#dc2626}

/* FUND TABLE */
.ft{width:100%;border-collapse:collapse}
.ft td{padding:5px 8px;border-bottom:1px solid #f8fafc;font-size:0.69rem}
.ft tr:hover td{background:#fef9f5}
.fl{color:#64748b;font-size:0.64rem}
.fv{color:#1e293b;text-align:right;font-family:'JetBrains Mono',monospace;font-size:0.69rem;font-weight:500}

/* SECTOR TILE */
.sec-t{background:#fff;border:1px solid #e2e8f0;border-radius:6px;
  padding:8px;text-align:center;box-shadow:0 1px 3px rgba(0,0,0,0.04)}
.sec-n{font-size:0.55rem;font-weight:500;color:#94a3b8;text-transform:uppercase;letter-spacing:0.06em}
.sec-p{font-family:'JetBrains Mono',monospace;font-size:0.82rem;font-weight:600;margin-top:3px}
.sec-p.pos{color:#16a34a}.sec-p.neg{color:#dc2626}

/* AI SECTIONS */
.ai-section{background:#fff;border:1px solid #e2e8f0;border-radius:9px;
  padding:16px 18px;margin-bottom:12px;box-shadow:0 1px 4px rgba(0,0,0,0.05)}
.ai-label{display:inline-flex;align-items:center;gap:6px;font-size:0.6rem;
  font-weight:600;letter-spacing:0.1em;text-transform:uppercase;
  padding:3px 10px;border-radius:20px;margin-bottom:10px}
.ai-label-full{background:#fff7ed;color:#f97316;border:1px solid #fed7aa}
.ai-label-news{background:#eff6ff;color:#2563eb;border:1px solid #bfdbfe}
.ai-label-tech{background:#f0fdf4;color:#16a34a;border:1px solid #bbf7d0}
.ai-label-fund{background:#fdf4ff;color:#9333ea;border:1px solid #e9d5ff}
.ai-label-fin{background:#fff1f2;color:#e11d48;border:1px solid #fecdd3}
.ai-title{font-size:0.88rem;font-weight:600;color:#0f172a;margin-bottom:12px}
.ai-body{font-size:0.74rem;color:#374151;line-height:1.8}
.ai-body p{margin-bottom:10px}
.ai-body strong{font-weight:600;color:#1e293b}
.ai-divider{height:1px;background:#f1f5f9;margin:14px 0}
.ai-disclaimer{font-size:0.57rem;color:#94a3b8;font-style:italic;margin-top:10px;padding-top:8px;border-top:1px solid #f1f5f9}
.ai-spinner{font-size:0.7rem;color:#94a3b8;font-family:'JetBrains Mono',monospace;padding:8px 0}

/* RIGHT PANEL ROWS */
.rr{display:flex;align-items:center;justify-content:space-between;
  padding:7px 13px;border-bottom:1px solid #f8fafc;cursor:pointer;transition:background 0.1s}
.rr:hover{background:#fef9f5}
.rr.rr-sel{background:#fff7ed;border-left:3px solid #f97316}
.rr-sym{font-family:'JetBrains Mono',monospace;font-size:0.7rem;font-weight:600;color:#1e293b}
.rr-nm{font-size:0.57rem;color:#94a3b8;margin-top:1px}
.rr-p{font-family:'JetBrains Mono',monospace;font-size:0.7rem;font-weight:500;color:#374151;text-align:right}
.rr-c{font-family:'JetBrains Mono',monospace;font-size:0.61rem;font-weight:500;text-align:right;margin-top:1px}
.rr-c.pos{color:#16a34a}.rr-c.neg{color:#dc2626}

/* expander — hide it completely */
details{display:none!important}

/* stDataFrame */
.stDataFrame{border-radius:7px!important;border:1px solid #e2e8f0!important;overflow:hidden!important}
[data-testid="stPlotlyChart"]{border-radius:7px;overflow:hidden}
</style>
""", unsafe_allow_html=True)

# ── TOPBAR ────────────────────────────────────────────────────────────────────
idx_q={i["sym"]:qget(i["sym"]) for i in INDICES}
chips=""
for i in INDICES:
    q=idx_q[i["sym"]]; arr,_=ud(q["pct"]); cls=sc(q["pct"])
    chips+=f"""<div class="ic"><span class="ic-n">{i['name']}</span>
      <span class="ic-v">{q['p']:,.2f}</span>
      <span class="ic-c {cls}">{arr} {abs(q['pct']):.2f}%</span></div>"""

st.markdown(f"""<div class="topbar">
  <span class="t-logo"><span class="t-dot">◈</span> DALAL</span>{chips}
  <div class="t-r"><span class="t-time">{now_str}</span>
  <span class="t-live">● LIVE</span></div></div>""", unsafe_allow_html=True)

L,C,R=st.columns([2.1,6.5,2.4])

# ══════════════════════════════════ LEFT ══════════════════════════════════════
with L:
    # ── SINGLE search box — type + Enter adds to watchlist ──
    st.markdown('<div class="sh">Add to Watchlist</div>', unsafe_allow_html=True)

    with st.form("add_form", clear_on_submit=True):
        add_inp = st.text_input("", placeholder="Type ticker or name, press Enter…",
                                key="ai_inp", label_visibility="collapsed")
        submitted = st.form_submit_button("Add", use_container_width=True)
        if submitted and add_inp.strip():
            raw = add_inp.strip()
            # Try exact ticker match first
            base_upper = raw.upper().replace(".NS","").replace(".BO","")
            if base_upper in NSE_STOCKS:
                sym = base_upper + ".NS"
                nm  = NSE_STOCKS[base_upper]
            else:
                # Try name search
                hits_add = do_search(raw)
                if hits_add:
                    sym = hits_add[0]["sym"] + ".NS"
                    nm  = hits_add[0]["name"]
                else:
                    sym = to_sym(raw)
                    nm  = raw.upper().replace(".NS","")
            e = {"sym": sym, "name": nm}
            if e not in st.session_state.watchlist:
                st.session_state.watchlist.append(e)
                st.session_state.sel      = sym
                st.session_state.sel_name = nm
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
        sel_cls = "wl-item wl-sel" if is_s else "wl-item"

        c1, c2 = st.columns([5, 1])
        with c1:
            # Single button styled to look like the row
            tp = "primary" if is_s else "secondary"
            label = f"{base}  {ps}  {pcs}"
            if st.button(label, key=f"ws_{i}", type=tp):
                st.session_state.sel      = w["sym"]
                st.session_state.sel_name = w["name"]
                # Clear AI cache when switching stock
                for ak in list(st.session_state.keys()):
                    if ak.startswith("ai_cache_"):
                        del st.session_state[ak]
                st.rerun()
        with c2:
            if st.button("✕", key=f"wd_{i}"):
                to_del = i

    if to_del is not None:
        st.session_state.watchlist.pop(to_del)
        syms=[w["sym"] for w in st.session_state.watchlist]
        if st.session_state.sel not in syms and syms:
            st.session_state.sel      = st.session_state.watchlist[0]["sym"]
            st.session_state.sel_name = st.session_state.watchlist[0]["name"]
        st.rerun()

    # ── News ──
    st.markdown('<div class="sh" style="margin-top:2px">News</div>', unsafe_allow_html=True)
    nk=st.text_input("", type="password", placeholder="NewsAPI key…",
                     key="nk_inp", label_visibility="collapsed")
    if nk: st.session_state.nkey=nk

    arts=news_get(st.session_state.nkey, f"India NSE BSE {st.session_state.sel_name}")
    if arts:
        for a in arts[:12]:
            src=(a.get("source",{}).get("name",""))[:22]
            ttl=(a.get("title",""))[:72]
            url=a.get("url","#")
            st.markdown(f"""<div class="ni" onclick="window.open('{url}','_blank')">
              <div class="ni-s">{src}</div><div class="ni-t">{ttl}</div>
              <div class="ni-d">{tago(a.get('publishedAt',''))}</div></div>""",
              unsafe_allow_html=True)
    else:
        st.markdown('<div style="padding:10px 13px;font-size:0.63rem;color:#94a3b8">Enter NewsAPI key above for live news.</div>',
                    unsafe_allow_html=True)

# ══════════════════════════════════ CENTER ════════════════════════════════════
with C:
    q   =qget(st.session_state.sel)
    info=iget(st.session_state.sel)
    arr,col=ud(q["pct"])
    p=q["p"]; ch=q["ch"]; pct=q["pct"]
    hi =q["hi"] or info.get("dayHigh") or 0
    lo =q["lo"] or info.get("dayLow")  or 0
    op_=info.get("open") or info.get("regularMarketOpen") or 0
    pc =q["pc"] or info.get("previousClose") or 0

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
          <div class="bn-chg" style="color:{col}">{arr} ₹{abs(ch):,.2f} ({abs(pct):.2f}%)</div>
        </div>
      </div></div>""", unsafe_allow_html=True)

    # ── Period + chart type ──
    btns=list(PERIODS.keys())+["Line","Candle","Area"]
    pcols=st.columns(len(btns))
    for i,lbl in enumerate(PERIODS.keys()):
        tp="primary" if st.session_state.period==lbl else "secondary"
        if pcols[i].button(lbl,key=f"pb_{lbl}",type=tp):
            st.session_state.period=lbl; st.rerun()
    for j,ct in enumerate(["Line","Candle","Area"]):
        tp="primary" if st.session_state.ctype==ct else "secondary"
        if pcols[len(PERIODS)+j].button(ct,key=f"cb_{ct}",type=tp):
            st.session_state.ctype=ct; st.rerun()

    # ── Chart ──
    pr,iv=PERIODS[st.session_state.period]
    df=hget(st.session_state.sel,pr,iv)
    is_pos=pct>=0; GRN,RED="#16a34a","#dc2626"
    lc=GRN if is_pos else RED
    fa="rgba(22,163,74,0.07)" if is_pos else "rgba(220,38,38,0.07)"

    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    if not df.empty and "Close" in df.columns:
        has_ohlc=all(c in df.columns for c in ["Open","High","Low","Close"])
        fig=make_subplots(rows=2,cols=1,shared_xaxes=True,row_heights=[0.74,0.26],vertical_spacing=0.02)
        ct=st.session_state.ctype
        if ct=="Candle" and has_ohlc:
            fig.add_trace(go.Candlestick(
                x=df.index,open=df["Open"],high=df["High"],low=df["Low"],close=df["Close"],
                increasing_line_color=GRN,decreasing_line_color=RED,
                name="OHLC",showlegend=False),row=1,col=1)
        elif ct=="Area":
            fig.add_trace(go.Scatter(x=df.index,y=df["Close"],mode="lines",
                line=dict(color=lc,width=1.5),fill="tozeroy",fillcolor=fa,
                name="Price",showlegend=False),row=1,col=1)
        else:
            fig.add_trace(go.Scatter(x=df.index,y=df["Close"],mode="lines",
                line=dict(color=lc,width=1.5),name="Price",showlegend=False),row=1,col=1)
        cf=df["Close"].astype(float)
        if len(df)>=20:
            fig.add_trace(go.Scatter(x=df.index,y=cf.rolling(20).mean(),mode="lines",
                line=dict(color="#f59e0b",width=1.2,dash="dot"),name="MA20",opacity=0.9),row=1,col=1)
        if len(df)>=50:
            fig.add_trace(go.Scatter(x=df.index,y=cf.rolling(50).mean(),mode="lines",
                line=dict(color="#6366f1",width=1.2,dash="dot"),name="MA50",opacity=0.9),row=1,col=1)
        if "Volume" in df.columns:
            vc=[GRN if float(c)>=float(o) else RED for c,o in zip(df["Close"],df.get("Open",df["Close"]))]
            fig.add_trace(go.Bar(x=df.index,y=df["Volume"],marker_color=vc,opacity=0.5,
                name="Vol",showlegend=False),row=2,col=1)
        ax=dict(showgrid=False,zeroline=False,color="#94a3b8",
                tickfont=dict(family="JetBrains Mono",size=10,color="#94a3b8"),linecolor="#e2e8f0")
        yax=dict(showgrid=True,gridcolor="#f1f5f9",zeroline=False,side="right",color="#94a3b8",
                 tickfont=dict(family="JetBrains Mono",size=10,color="#94a3b8"))
        fig.update_layout(
            paper_bgcolor="rgba(255,255,255,0)",plot_bgcolor="rgba(255,255,255,0)",
            margin=dict(l=0,r=4,t=4,b=0),height=320,showlegend=True,
            legend=dict(orientation="h",y=1.05,x=0,
                font=dict(family="JetBrains Mono",size=10,color="#94a3b8"),bgcolor="rgba(0,0,0,0)"),
            hovermode="x unified",
            hoverlabel=dict(bgcolor="#fff",bordercolor="#e2e8f0",
                font=dict(family="JetBrains Mono",size=11,color="#1e293b")),
            xaxis=dict(**ax),xaxis2=dict(**ax,rangeslider=dict(visible=False)),
            yaxis=dict(**yax),yaxis2=dict(showgrid=False,showticklabels=False),
        )
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    else:
        st.markdown('<div style="height:250px;display:flex;align-items:center;justify-content:center;color:#94a3b8;font-size:0.75rem">No chart data available</div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

    # ── DATA TABS ──
    dtabs=["Overview","Fundamentals","Financials","Sectors"]
    tc=st.columns(len(dtabs))
    for i,t in enumerate(dtabs):
        tp="primary" if st.session_state.ctab==t else "secondary"
        if tc[i].button(t,key=f"ct_{t}",type=tp):
            st.session_state.ctab=t; st.rerun()

    if st.session_state.ctab=="Overview":
        st.markdown('<div class="sct">Key Metrics</div>',unsafe_allow_html=True)
        mcap=info.get("marketCap"); wh52=info.get("fiftyTwoWeekHigh")
        wl52=info.get("fiftyTwoWeekLow"); pe_=info.get("trailingPE")
        fpe=info.get("forwardPE"); eps=info.get("trailingEps")
        dy=info.get("dividendYield"); vol=info.get("volume") or info.get("regularMarketVolume")
        avol=info.get("averageVolume"); beta=info.get("beta"); ptb=info.get("priceToBook")
        wk52pct=round((p-wl52)/(wh52-wl52)*100,1) if (wh52 and wl52 and p and wh52!=wl52) else None
        metrics=[
            ("Market Cap",  finr(mcap),  ""),
            ("52W High",    sv(wh52),    "pos" if p and wh52 and p>=wh52*0.95 else ""),
            ("52W Low",     sv(wl52),    "neg" if p and wl52 and p<=wl52*1.05 else ""),
            ("52W Range",   f"{wk52pct:.0f}%" if wk52pct is not None else "—",""),
            ("P/E (TTM)",   sv(pe_,"",dec=1),""),
            ("Fwd P/E",     sv(fpe,"",dec=1),""),
            ("EPS (TTM)",   sv(eps),     ""),
            ("Div Yield",   sv(dy,fmt="pct"),"pos" if dy and float(dy)>0 else ""),
            ("Volume",      sv(vol,fmt="vol"),""),
            ("Avg Volume",  sv(avol,fmt="vol"),""),
            ("Beta",        sv(beta,"",dec=2),""),
            ("Price/Book",  sv(ptb,"",dec=2),""),
        ]
        mc4=st.columns(4)
        for idx_,(lbl,val,vc) in enumerate(metrics):
            mvc=f"mc-v {vc}".strip()
            with mc4[idx_%4]:
                st.markdown(f'<div class="mc"><div class="mc-l">{lbl}</div><div class="{mvc}">{val}</div></div>',unsafe_allow_html=True)

    elif st.session_state.ctab=="Fundamentals":
        roe=info.get("returnOnEquity"); roa=info.get("returnOnAssets")
        gm=info.get("grossMargins"); om=info.get("operatingMargins"); pm=info.get("profitMargins")
        d2e=info.get("debtToEquity"); cr=info.get("currentRatio"); fcf=info.get("freeCashflow")
        rev=info.get("totalRevenue"); ebit=info.get("ebitda"); ni=info.get("netIncomeToCommon")
        eg=info.get("earningsGrowth"); rg=info.get("revenueGrowth"); bv=info.get("bookValue")
        td=info.get("totalDebt"); tc_=info.get("totalCash")
        shr=info.get("sharesOutstanding"); evr=info.get("enterpriseToRevenue"); eve=info.get("enterpriseToEbitda")
        qeg=info.get("earningsQuarterlyGrowth")
        fa2,fb2=st.columns(2)
        with fa2:
            st.markdown('<div class="sct">Profitability</div>',unsafe_allow_html=True)
            rows1=[("Revenue",finr(rev)),("EBITDA",finr(ebit)),("Net Income",finr(ni)),
                   ("Free Cash Flow",finr(fcf)),("Gross Margin",sv(gm,fmt="pct")),
                   ("Operating Margin",sv(om,fmt="pct")),("Net Margin",sv(pm,fmt="pct")),
                   ("ROE",sv(roe,fmt="pct")),("ROA",sv(roa,fmt="pct")),
                   ("EV/Revenue",sv(evr,"",dec=2)),("EV/EBITDA",sv(eve,"",dec=2)),
                   ("Rev Growth YoY",sv(rg,fmt="pct")),("Earn Growth YoY",sv(eg,fmt="pct")),
                   ("Earn Growth QoQ",sv(qeg,fmt="pct"))]
            st.markdown('<table class="ft">',unsafe_allow_html=True)
            for lbl,val in rows1:
                st.markdown(f'<tr><td class="fl">{lbl}</td><td class="fv">{val}</td></tr>',unsafe_allow_html=True)
            st.markdown('</table>',unsafe_allow_html=True)
        with fb2:
            st.markdown('<div class="sct">Balance Sheet</div>',unsafe_allow_html=True)
            nd_=finr(float(td)-float(tc_)) if (td and tc_) else "—"
            rows2=[("Total Debt",finr(td)),("Total Cash",finr(tc_)),("Net Debt",nd_),
                   ("Debt/Equity",sv(d2e,"",dec=2)),("Current Ratio",sv(cr,"",dec=2)),
                   ("Book Value/Share",sv(bv,dec=2)),("Shares Outstanding",sv(shr,fmt="vol")),
                   ("Float Shares",sv(info.get("floatShares"),fmt="vol"))]
            st.markdown('<table class="ft">',unsafe_allow_html=True)
            for lbl,val in rows2:
                st.markdown(f'<tr><td class="fl">{lbl}</td><td class="fv">{val}</td></tr>',unsafe_allow_html=True)
            st.markdown('</table>',unsafe_allow_html=True)
            st.markdown('<div class="sct" style="margin-top:8px">Company</div>',unsafe_allow_html=True)
            ci=[("Sector",info.get("sector","—")),("Industry",info.get("industry","—")),
                ("Exchange",info.get("exchange","—")),("Country",info.get("country","India"))]
            st.markdown('<table class="ft">',unsafe_allow_html=True)
            for lbl,val in ci:
                st.markdown(f'<tr><td class="fl">{lbl}</td><td class="fv">{val}</td></tr>',unsafe_allow_html=True)
            st.markdown('</table>',unsafe_allow_html=True)
        summary=info.get("longBusinessSummary","")
        if summary:
            st.markdown(f'<div style="font-size:0.67rem;color:#64748b;line-height:1.65;margin-top:8px;padding:11px 13px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:6px">{summary[:700]}…</div>',unsafe_allow_html=True)

    elif st.session_state.ctab=="Financials":
        fin_d,bs_d,cf_d=fget(st.session_state.sel)
        def rend_fin(df_in,label):
            if df_in is None or df_in.empty:
                st.markdown(f'<div style="padding:8px;color:#94a3b8;font-size:0.63rem">{label}: not available</div>',unsafe_allow_html=True); return
            st.markdown(f'<div class="sct">{label}</div>',unsafe_allow_html=True)
            d=df_in.head(10).copy()
            d.index=[str(x)[:38] for x in d.index]; d.columns=[str(c)[:12] for c in d.columns]
            def fc(x):
                try:
                    f=float(x)
                    if abs(f)>=1e7: return f"₹{f/1e7:.1f}Cr"
                    if abs(f)>=1e5: return f"₹{f/1e5:.1f}L"
                    return f"₹{f:,.0f}"
                except: return "—"
            st.dataframe(d.map(fc),use_container_width=True)
        rend_fin(fin_d,"Income Statement (Annual)")
        rend_fin(bs_d,"Balance Sheet (Annual)")
        rend_fin(cf_d,"Cash Flow (Annual)")

    elif st.session_state.ctab=="Sectors":
        st.markdown('<div class="sct">Sector Performance Today</div>',unsafe_allow_html=True)
        sc4=st.columns(4)
        for i,s in enumerate(SECTORS):
            qs=qget(s["sym"]); arr_s,_=ud(qs["pct"]); cls_s=sc(qs["pct"])
            with sc4[i%4]:
                st.markdown(f'<div class="sec-t"><div class="sec-n">{s["name"]}</div><div class="sec-p {cls_s}">{arr_s} {abs(qs["pct"]):.2f}%</div></div>',unsafe_allow_html=True)
        st.markdown('<div class="sct" style="margin-top:12px">1-Month Normalised Return (%)</div>',unsafe_allow_html=True)
        sfig=go.Figure()
        pal=["#16a34a","#2563eb","#d97706","#9333ea","#dc2626","#0891b2","#f97316","#65a30d"]
        for si,s in enumerate(SECTORS):
            sdf=hget(s["sym"],"1mo","1d")
            if not sdf.empty and "Close" in sdf.columns and len(sdf)>1:
                base=float(sdf["Close"].iloc[0]); norm=(sdf["Close"].astype(float)/base-1)*100
                sfig.add_trace(go.Scatter(x=sdf.index,y=norm.round(2),mode="lines",
                    name=s["name"],line=dict(color=pal[si],width=1.5)))
        sfig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0,r=4,t=4,b=0),height=220,hovermode="x unified",
            legend=dict(orientation="h",y=1.1,font=dict(family="JetBrains Mono",size=10,color="#64748b"),bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(showgrid=False,zeroline=False,color="#94a3b8",tickfont=dict(family="JetBrains Mono",size=10,color="#94a3b8")),
            yaxis=dict(showgrid=True,gridcolor="#f1f5f9",zeroline=True,zerolinecolor="#e2e8f0",
                side="right",ticksuffix="%",tickfont=dict(family="JetBrains Mono",size=10,color="#94a3b8")),
            hoverlabel=dict(bgcolor="#fff",bordercolor="#e2e8f0",font=dict(family="JetBrains Mono",size=11,color="#1e293b")),
        )
        st.plotly_chart(sfig,use_container_width=True,config={"displayModeBar":False})

    # ══════════════ AI ANALYSIS — AUTO-GENERATED, NO TABS ══════════════════════
    st.markdown('<div class="sct" style="margin-top:16px">AI Analysis</div>', unsafe_allow_html=True)

    ticker    = st.session_state.sel
    sym_label = st.session_state.sel_name

    # Gather all data for AI
    tech_df  = hget(ticker, "1y", "1d")
    technicals = calc_technicals(tech_df)
    fin_ai, bs_ai, cf_ai = fget(ticker)

    def df_to_txt(df_in, label, rows=7):
        if df_in is None or df_in.empty: return f"{label}: not available\n"
        d=df_in.head(rows).copy()
        d.index=[str(x)[:35] for x in d.index]; d.columns=[str(c)[:10] for c in d.columns]
        def fc(x):
            try:
                f=float(x)
                if abs(f)>=1e7: return f"₹{f/1e7:.1f}Cr"
                if abs(f)>=1e5: return f"₹{f/1e5:.1f}L"
                return f"₹{f:,.0f}"
            except: return str(x)
        return f"{label}:\n{d.map(fc).to_string()}\n\n"

    fin_txt = df_to_txt(fin_ai,"Income Statement")
    bs_txt  = df_to_txt(bs_ai,"Balance Sheet")
    cf_txt  = df_to_txt(cf_ai,"Cash Flow")

    arts_ai = news_get(st.session_state.nkey, f"India NSE BSE {sym_label}") if st.session_state.nkey else []
    news_txt = "\n".join([f"- {a.get('title','')} ({a.get('source',{}).get('name','')}, {tago(a.get('publishedAt',''))})"
                          for a in arts_ai[:10]]) if arts_ai else "No news available."

    fund_keys=["marketCap","trailingPE","forwardPE","trailingEps","dividendYield",
               "returnOnEquity","returnOnAssets","grossMargins","operatingMargins",
               "profitMargins","debtToEquity","currentRatio","freeCashflow",
               "totalRevenue","ebitda","netIncomeToCommon","earningsGrowth",
               "revenueGrowth","bookValue","priceToBook","beta",
               "fiftyTwoWeekHigh","fiftyTwoWeekLow","enterpriseToRevenue",
               "enterpriseToEbitda","sector","industry"]
    fund_txt="\n".join([f"  {k}: {info.get(k)}" for k in fund_keys if info.get(k) is not None])
    tech_txt="\n".join([f"  {k}: {v}" for k,v in technicals.items()])
    price_ctx=(f"Price: ₹{p:,.2f} | Change: {ch:+.2f} ({pct:+.2f}%) | "
               f"O:₹{op_:,.2f} H:₹{hi:,.2f} L:₹{lo:,.2f} PC:₹{pc:,.2f} | "
               f"Sector: {info.get('sector','—')}")

    AI_ANALYSES = [
        {
            "key": "full",
            "label_cls": "ai-label-full",
            "label_txt": "🤖 Full Analysis",
            "title": f"Comprehensive Stock Analysis — {sym_label}",
            "prompt": f"""You are a senior equity analyst at an Indian investment bank. Write a comprehensive, institutional-quality research note on {sym_label} ({ticker}).

PRICE: {price_ctx}
TECHNICALS: {tech_txt}
FUNDAMENTALS: {fund_txt}
FINANCIALS: {fin_txt}{bs_txt}{cf_txt}
NEWS: {news_txt}

Write flowing paragraphs (no bullet points, no numbered lists). Cover: executive summary and verdict, price action and momentum, technical setup, fundamental quality and valuation, financial health, news sentiment impact, key risks, and a clear BUY / HOLD / SELL conclusion with reasoning. Be specific with numbers. Be bold. Write like a Goldman Sachs research note. 400-500 words.""",
        },
        {
            "key": "news",
            "label_cls": "ai-label-news",
            "label_txt": "📰 News Analysis",
            "title": f"News & Sentiment — {sym_label}",
            "prompt": f"""You are a financial news analyst specialising in Indian equity markets. Analyse the following news headlines for {sym_label} ({ticker}).

STOCK CONTEXT: {price_ctx}
NEWS HEADLINES:
{news_txt}

Write 3-4 flowing paragraphs (no bullet points). Cover: overall news sentiment and why, dominant themes and narratives, any near-term catalysts or risks from the news, whether headlines are already priced in or represent a divergence from current price, and trading implication from this news flow alone. If no news is available, comment on what news would matter most for this stock. 200-250 words.""",
        },
        {
            "key": "tech",
            "label_cls": "ai-label-tech",
            "label_txt": "📈 Technical Analysis",
            "title": f"Technical Analysis — {sym_label}",
            "prompt": f"""You are a professional technical analyst with deep expertise in Indian equity markets (NSE/BSE). Analyse the following technical data for {sym_label} ({ticker}).

PRICE DATA: {price_ctx}
TECHNICAL INDICATORS:
{tech_txt}

Write 3-4 flowing paragraphs (no bullet points). Cover: primary trend direction and strength, moving average positions and what crossovers signal, RSI and momentum interpretation, MACD signal and histogram trend, Bollinger Band positioning (squeeze/expansion/breakout), volume conviction analysis, key support and resistance levels implied by the data, and end with a clear BULLISH / BEARISH / NEUTRAL signal, confidence level, and suggested entry zone with stop-loss. 200-250 words.""",
        },
        {
            "key": "fund",
            "label_cls": "ai-label-fund",
            "label_txt": "🏛 Fundamental Analysis",
            "title": f"Fundamental Analysis — {sym_label}",
            "prompt": f"""You are a fundamental equity analyst specialising in Indian listed companies. Provide a rigorous fundamental analysis of {sym_label} ({ticker}).

MARKET DATA: {price_ctx}
FUNDAMENTAL DATA:
{fund_txt}

Write 3-4 flowing paragraphs (no bullet points). Cover: business quality assessment from margins and return ratios, growth trajectory (revenue and earnings), valuation assessment (P/E, forward P/E, P/B, EV/EBITDA vs sector), capital efficiency and ROE quality, dividend and capital allocation, competitive moat implied by the numbers, and a clear fundamental verdict — STRONG BUY / BUY / HOLD / REDUCE / SELL with specific reasoning. Benchmark against Indian market averages. 200-250 words.""",
        },
        {
            "key": "fin",
            "label_cls": "ai-label-fin",
            "label_txt": "💰 Financial Analysis",
            "title": f"Financial Statement Analysis — {sym_label}",
            "prompt": f"""You are a CFA-qualified financial statement analyst. Conduct a forensic financial analysis of {sym_label} ({ticker}).

MARKET CONTEXT: {price_ctx}
INCOME STATEMENT: {fin_txt}
BALANCE SHEET: {bs_txt}
CASH FLOW: {cf_txt}
KEY RATIOS: {fund_txt}

Write 3-4 flowing paragraphs (no bullet points). Cover: revenue quality and growth consistency, earnings quality and cash conversion ratio, margin trajectory (gross/operating/net), free cash flow generation and capex intensity, balance sheet strength (debt levels, liquidity, net debt/EBITDA), working capital efficiency, any accounting red flags or inconsistencies between P&L and cash flow, and a financial health score out of 10 with clear justification. 200-250 words.""",
        },
    ]

    # Auto-generate each analysis — run on stock change
    for analysis in AI_ANALYSES:
        cache_key = f"ai_cache_{analysis['key']}_{ticker}"

        if cache_key not in st.session_state:
            with st.spinner(f"Generating {analysis['label_txt']}…"):
                result = call_claude(analysis["prompt"])
            st.session_state[cache_key] = result

        result = st.session_state[cache_key]

        st.markdown(f"""<div class="ai-section">
          <div class="ai-label {analysis['label_cls']}">{analysis['label_txt']}</div>
          <div class="ai-title">{analysis['title']}</div>
          <div class="ai-body">{result.replace(chr(10), '<br>')}</div>
          <div class="ai-disclaimer">AI-generated analysis for informational purposes only. Not financial advice.</div>
        </div>""", unsafe_allow_html=True)

        if analysis["key"] != "fin":
            st.markdown('<div class="ai-divider"></div>', unsafe_allow_html=True)


# ══════════════════════════════════ RIGHT ═════════════════════════════════════
with R:
    RTABS=["Gainers","Losers","Indices","Commodities","MCX"]
    rtc=st.columns(len(RTABS))
    for i,t in enumerate(RTABS):
        tp="primary" if st.session_state.rtab==t else "secondary"
        if rtc[i].button(t,key=f"rt_{t}",type=tp):
            st.session_state.rtab=t; st.rerun()

    tab=st.session_state.rtab

    if tab in ("Gainers","Losers"):
        rows=[]
        for sym in NIFTY50:
            qr=qget(sym); base=sym.replace(".NS","")
            rows.append({"sym":base,"full":sym,"name":NSE_STOCKS.get(base,base),"p":qr["p"],"pct":qr["pct"]})
        rows.sort(key=lambda x:x["pct"],reverse=(tab=="Gainers"))
        for r in rows[:20]:
            arr_r,_=ud(r["pct"]); cls_r=sc(r["pct"])
            ps=f"₹{r['p']:,.2f}" if r["p"] else "—"
            sel="rr rr-sel" if r["full"]==st.session_state.sel else "rr"
            st.markdown(f"""<div class="{sel}"><div>
              <div class="rr-sym">{r['sym']}</div>
              <div class="rr-nm">{r['name'][:22]}</div>
            </div><div>
              <div class="rr-p">{ps}</div>
              <div class="rr-c {cls_r}">{arr_r} {abs(r['pct']):.2f}%</div>
            </div></div>""",unsafe_allow_html=True)
            if st.button(f"View {r['sym']}",key=f"rs_{tab}_{r['sym']}",use_container_width=True):
                st.session_state.sel=r["full"]; st.session_state.sel_name=r["name"]
                for ak in list(st.session_state.keys()):
                    if ak.startswith("ai_cache_"): del st.session_state[ak]
                st.rerun()

    elif tab=="Indices":
        for ix in ALL_IDX:
            qi=qget(ix["sym"]); arr_i,_=ud(qi["pct"]); cls_i=sc(qi["pct"])
            ps=f"{qi['p']:,.2f}" if qi["p"] else "—"
            sel="rr rr-sel" if ix["sym"]==st.session_state.sel else "rr"
            st.markdown(f"""<div class="{sel}"><div><div class="rr-sym">{ix['name']}</div></div>
              <div><div class="rr-p">{ps}</div><div class="rr-c {cls_i}">{arr_i} {abs(qi['pct']):.2f}%</div></div>
            </div>""",unsafe_allow_html=True)
            if st.button(f"View {ix['name'][:14]}",key=f"ri_{ix['sym']}",use_container_width=True):
                st.session_state.sel=ix["sym"]; st.session_state.sel_name=ix["name"]
                for ak in list(st.session_state.keys()):
                    if ak.startswith("ai_cache_"): del st.session_state[ak]
                st.rerun()

    elif tab=="Commodities":
        for c in COMMODITIES:
            qc=qget(c["sym"]); arr_c,_=ud(qc["pct"]); cls_c=sc(qc["pct"])
            ps=f"{qc['p']:,.2f}" if qc["p"] else "—"
            sel="rr rr-sel" if c["sym"]==st.session_state.sel else "rr"
            st.markdown(f"""<div class="{sel}"><div><div class="rr-sym">{c['name']}</div></div>
              <div><div class="rr-p">{ps}</div><div class="rr-c {cls_c}">{arr_c} {abs(qc['pct']):.2f}%</div></div>
            </div>""",unsafe_allow_html=True)
            if st.button(f"View {c['name'][:14]}",key=f"rc_{c['sym']}",use_container_width=True):
                st.session_state.sel=c["sym"]; st.session_state.sel_name=c["name"]
                for ak in list(st.session_state.keys()):
                    if ak.startswith("ai_cache_"): del st.session_state[ak]
                st.rerun()

    elif tab=="MCX":
        for m in MCX_LIST:
            qm=qget(m["sym"]); arr_m,_=ud(qm["pct"]); cls_m=sc(qm["pct"])
            bm=m["sym"].replace(".NS","")
            ps=f"₹{qm['p']:,.2f}" if qm["p"] else "—"
            sel="rr rr-sel" if m["sym"]==st.session_state.sel else "rr"
            st.markdown(f"""<div class="{sel}"><div>
              <div class="rr-sym">{bm}</div><div class="rr-nm">{m['name']}</div>
            </div><div>
              <div class="rr-p">{ps}</div><div class="rr-c {cls_m}">{arr_m} {abs(qm['pct']):.2f}%</div>
            </div></div>""",unsafe_allow_html=True)
            if st.button(f"View {bm[:14]}",key=f"rm_{m['sym']}",use_container_width=True):
                st.session_state.sel=m["sym"]; st.session_state.sel_name=m["name"]
                for ak in list(st.session_state.keys()):
                    if ak.startswith("ai_cache_"): del st.session_state[ak]
                st.rerun()

    # Sparkline
    st.markdown("<hr style='border:none;border-top:1px solid #f1f5f9;margin:6px 0'>",unsafe_allow_html=True)
    mdf=hget(st.session_state.sel,"1mo","1d")
    if not mdf.empty and "Close" in mdf.columns:
        lc_m=GRN if pct>=0 else RED
        fa_m="rgba(22,163,74,0.1)" if pct>=0 else "rgba(220,38,38,0.1)"
        mfig=go.Figure(go.Scatter(x=mdf.index,y=mdf["Close"].astype(float),
            mode="lines",line=dict(color=lc_m,width=1.5),fill="tozeroy",fillcolor=fa_m))
        mfig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0,r=0,t=0,b=0),height=52,showlegend=False,
            xaxis=dict(visible=False),yaxis=dict(visible=False))
        slbl=st.session_state.sel.replace(".NS","").replace(".BO","")
        st.markdown(f'<div style="font-size:0.54rem;color:#94a3b8;padding:3px 8px;font-family:JetBrains Mono,monospace;text-transform:uppercase;letter-spacing:0.1em">{slbl} · 1M</div>',unsafe_allow_html=True)
        st.plotly_chart(mfig,use_container_width=True,config={"displayModeBar":False})

    st.markdown("<hr style='border:none;border-top:1px solid #f1f5f9;margin:6px 0'>",unsafe_allow_html=True)
    if st.button("⟳ Refresh Data",use_container_width=True):
        st.cache_data.clear()
        for ak in list(st.session_state.keys()):
            if ak.startswith("ai_cache_"): del st.session_state[ak]
        st.rerun()
    st.markdown('<div style="font-size:0.52rem;color:#cbd5e1;text-align:center;padding:4px;font-family:JetBrains Mono,monospace">Yahoo Finance · 2min cache · ~15min delay</div>',unsafe_allow_html=True)
