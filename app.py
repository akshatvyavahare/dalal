import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BHARAT TERMINAL",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── STYLE ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Sora:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
  font-family: 'Sora', sans-serif;
  background: #0c0e14;
  color: #dde1ea;
}
.main .block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none; }
#MainMenu, footer, header, [data-testid="stToolbar"], .stDeployButton { display: none !important; }
::-webkit-scrollbar { width: 3px; background: transparent; }
::-webkit-scrollbar-thumb { background: #2a2d3a; border-radius: 2px; }

/* ── LAYOUT SHELL ── */
.shell {
  display: grid;
  grid-template-columns: 240px 1fr 280px;
  grid-template-rows: 52px 1fr;
  height: 100vh;
  overflow: hidden;
  background: #0c0e14;
}

/* ── TOPBAR ── */
.topbar {
  grid-column: 1 / -1;
  display: flex;
  align-items: center;
  padding: 0 20px;
  background: #0f1118;
  border-bottom: 1px solid #1e2130;
  gap: 28px;
}
.logo {
  font-family: 'DM Mono', monospace;
  font-size: 0.9rem;
  font-weight: 500;
  color: #f97316;
  letter-spacing: 0.15em;
  white-space: nowrap;
  margin-right: 8px;
}
.index-chip {
  display: flex;
  flex-direction: column;
  padding: 2px 14px;
  border-radius: 4px;
  background: #161820;
  border: 1px solid #1e2130;
  cursor: default;
}
.index-chip .ic-name { font-size: 0.58rem; color: #6b7280; letter-spacing: 0.08em; text-transform: uppercase; font-family: 'DM Mono', monospace; }
.index-chip .ic-val  { font-size: 0.82rem; font-weight: 500; color: #e5e7eb; font-family: 'DM Mono', monospace; }
.index-chip .ic-chg.up   { font-size: 0.65rem; color: #22c55e; }
.index-chip .ic-chg.down { font-size: 0.65rem; color: #ef4444; }
.topbar-time { margin-left: auto; font-family: 'DM Mono', monospace; font-size: 0.65rem; color: #4b5563; }
.topbar-live { font-family: 'DM Mono', monospace; font-size: 0.62rem; color: #22c55e; border: 1px solid #22c55e33; padding: 2px 8px; border-radius: 2px; }

/* ── LEFT PANEL ── */
.left-panel {
  background: #0f1118;
  border-right: 1px solid #1e2130;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}
.panel-section { padding: 14px 14px 8px; }
.panel-title {
  font-family: 'DM Mono', monospace;
  font-size: 0.6rem;
  color: #4b5563;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.panel-title span { color: #f97316; cursor: pointer; font-size: 0.7rem; }

.wl-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 7px 8px;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.1s;
  margin-bottom: 2px;
}
.wl-row:hover, .wl-row.active { background: #161a26; }
.wl-row .sym  { font-family: 'DM Mono', monospace; font-size: 0.78rem; font-weight: 500; color: #e5e7eb; }
.wl-row .name { font-size: 0.6rem; color: #6b7280; margin-top: 1px; }
.wl-row .price { font-family: 'DM Mono', monospace; font-size: 0.78rem; color: #e5e7eb; text-align: right; }
.wl-row .chg   { font-family: 'DM Mono', monospace; font-size: 0.62rem; text-align: right; padding: 1px 5px; border-radius: 3px; margin-top: 2px; font-weight: 500; }
.chg.up   { color: #22c55e; background: #14532d22; }
.chg.down { color: #ef4444; background: #7f1d1d22; }

.divider { height: 1px; background: #1e2130; margin: 8px 0; }

/* ── NEWS ITEMS ── */
.news-item {
  padding: 8px 14px;
  border-bottom: 1px solid #1a1d28;
  cursor: pointer;
  transition: background 0.1s;
}
.news-item:hover { background: #131620; }
.news-src  { font-family: 'DM Mono', monospace; font-size: 0.58rem; color: #f97316; margin-bottom: 2px; letter-spacing: 0.06em; text-transform: uppercase; }
.news-head { font-size: 0.72rem; color: #c9d1db; line-height: 1.4; }
.news-time { font-family: 'DM Mono', monospace; font-size: 0.58rem; color: #374151; margin-top: 3px; }

/* ── CENTER PANEL ── */
.center-panel {
  overflow-y: auto;
  padding: 16px 18px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.stock-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
}
.stock-title { font-size: 1.1rem; font-weight: 600; color: #f3f4f6; }
.stock-sub   { font-size: 0.7rem; color: #6b7280; margin-top: 2px; }
.stock-price { font-family: 'DM Mono', monospace; font-size: 2rem; font-weight: 500; color: #f3f4f6; line-height: 1; }
.stock-chg-big { font-family: 'DM Mono', monospace; font-size: 0.85rem; margin-top: 4px; }
.stock-chg-big.up   { color: #22c55e; }
.stock-chg-big.down { color: #ef4444; }

.period-bar {
  display: flex;
  gap: 6px;
  align-items: center;
}
.period-btn {
  font-family: 'DM Mono', monospace;
  font-size: 0.68rem;
  padding: 4px 10px;
  border-radius: 4px;
  border: 1px solid #1e2130;
  background: transparent;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.1s;
}
.period-btn.active, .period-btn:hover {
  background: #f97316;
  color: #0c0e14;
  border-color: #f97316;
  font-weight: 500;
}

.metrics-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
}
.metric-card {
  background: #0f1118;
  border: 1px solid #1e2130;
  border-radius: 6px;
  padding: 10px 12px;
}
.metric-label { font-size: 0.6rem; color: #6b7280; text-transform: uppercase; letter-spacing: 0.08em; font-family: 'DM Mono', monospace; }
.metric-value { font-family: 'DM Mono', monospace; font-size: 0.88rem; font-weight: 500; color: #e5e7eb; margin-top: 4px; }

.section-hdr {
  font-family: 'DM Mono', monospace;
  font-size: 0.62rem;
  color: #4b5563;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  padding-bottom: 8px;
  border-bottom: 1px solid #1e2130;
  margin-bottom: 10px;
}

/* ── RIGHT PANEL ── */
.right-panel {
  background: #0f1118;
  border-left: 1px solid #1e2130;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.tab-bar {
  display: flex;
  border-bottom: 1px solid #1e2130;
  padding: 0 14px;
}
.tab {
  font-family: 'DM Mono', monospace;
  font-size: 0.65rem;
  padding: 10px 10px;
  color: #6b7280;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  transition: all 0.1s;
  white-space: nowrap;
}
.tab.active { color: #f97316; border-bottom-color: #f97316; }
.tab:hover  { color: #e5e7eb; }

.gainer-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 7px 14px;
  border-bottom: 1px solid #13161f;
}
.gainer-row:hover { background: #131620; }
.gr-sym  { font-family: 'DM Mono', monospace; font-size: 0.75rem; font-weight: 500; color: #e5e7eb; }
.gr-name { font-size: 0.6rem; color: #6b7280; }
.gr-price { font-family: 'DM Mono', monospace; font-size: 0.75rem; color: #e5e7eb; text-align: right; }
.gr-chg  { font-family: 'DM Mono', monospace; font-size: 0.68rem; text-align: right; font-weight: 500; }
.gr-chg.up   { color: #22c55e; }
.gr-chg.down { color: #ef4444; }

.mkt-overview-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 14px;
  border-bottom: 1px solid #13161f;
}
.mo-label { font-size: 0.72rem; color: #9ca3af; }
.mo-val   { font-family: 'DM Mono', monospace; font-size: 0.72rem; color: #e5e7eb; }
.mo-chg   { font-family: 'DM Mono', monospace; font-size: 0.65rem; }
.mo-chg.up   { color: #22c55e; }
.mo-chg.down { color: #ef4444; }

/* Streamlit overrides */
[data-testid="stPlotlyChart"] { border-radius: 6px; overflow: hidden; }
.stSpinner { display: none; }
</style>
""", unsafe_allow_html=True)


# ─── DATA ─────────────────────────────────────────────────────────────────────
WATCHLIST_DEFAULT = [
    {"sym": "RELIANCE.NS",  "name": "Reliance Industries"},
    {"sym": "TCS.NS",       "name": "Tata Consultancy"},
    {"sym": "HDFCBANK.NS",  "name": "HDFC Bank"},
    {"sym": "INFY.NS",      "name": "Infosys"},
    {"sym": "ICICIBANK.NS", "name": "ICICI Bank"},
    {"sym": "WIPRO.NS",     "name": "Wipro"},
    {"sym": "SBIN.NS",      "name": "State Bank of India"},
    {"sym": "TATAMOTORS.NS","name": "Tata Motors"},
]

INDICES = [
    {"sym": "^NSEI",   "name": "NIFTY 50"},
    {"sym": "^BSESN",  "name": "SENSEX"},
    {"sym": "^NSMIDCP","name": "NIFTY MID"},
    {"sym": "^CNXIT",  "name": "NIFTY IT"},
    {"sym": "^CNXBANK","name": "BANK NIFTY"},
]

COMMODITIES = [
    {"sym": "GC=F",  "name": "Gold ($/oz)"},
    {"sym": "SI=F",  "name": "Silver ($/oz)"},
    {"sym": "CL=F",  "name": "Crude Oil"},
    {"sym": "NG=F",  "name": "Natural Gas"},
    {"sym": "USDINR=X", "name": "USD/INR"},
]

MCX_STOCKS = [
    {"sym": "TATASTEEL.NS", "name": "Tata Steel"},
    {"sym": "HINDALCO.NS",  "name": "Hindalco"},
    {"sym": "JSWSTEEL.NS",  "name": "JSW Steel"},
    {"sym": "ONGC.NS",      "name": "ONGC"},
    {"sym": "BPCL.NS",      "name": "BPCL"},
    {"sym": "IOC.NS",       "name": "Indian Oil"},
]

SECTOR_ETFS = [
    {"sym": "^CNXIT",    "name": "IT"},
    {"sym": "^CNXBANK",  "name": "Banking"},
    {"sym": "^CNXPHARMA","name": "Pharma"},
    {"sym": "^CNXFMCG",  "name": "FMCG"},
    {"sym": "^CNXAUTO",  "name": "Auto"},
    {"sym": "^CNXREALTY","name": "Realty"},
    {"sym": "^CNXMETAL", "name": "Metal"},
    {"sym": "^CNXENERGY","name": "Energy"},
]

PERIODS = {"1D": ("1d","2m"), "1W": ("5d","15m"), "1M": ("1mo","1h"), "3M": ("3mo","1d"), "6M": ("6mo","1d"), "1Y": ("1y","1d"), "3Y": ("3y","1wk")}
CHART_TYPES = ["Line", "Candle", "Area"]

# ─── SESSION STATE ─────────────────────────────────────────────────────────────
if "watchlist"    not in st.session_state: st.session_state.watchlist = WATCHLIST_DEFAULT.copy()
if "selected_sym" not in st.session_state: st.session_state.selected_sym = "RELIANCE.NS"
if "selected_name"not in st.session_state: st.session_state.selected_name = "Reliance Industries"
if "period"       not in st.session_state: st.session_state.period = "1M"
if "chart_type"   not in st.session_state: st.session_state.chart_type = "Area"
if "right_tab"    not in st.session_state: st.session_state.right_tab = "Gainers"
if "news_key"     not in st.session_state: st.session_state.news_key = ""
if "add_sym"      not in st.session_state: st.session_state.add_sym = ""


# ─── HELPERS ──────────────────────────────────────────────────────────────────
@st.cache_data(ttl=120)
def get_quote(sym):
    try:
        t = yf.Ticker(sym)
        info = t.fast_info
        price = round(info.last_price, 2)
        prev  = round(info.previous_close, 2)
        chg   = round(price - prev, 2)
        pct   = round((chg / prev) * 100, 2) if prev else 0
        return {"price": price, "chg": chg, "pct": pct, "prev": prev}
    except:
        return {"price": 0, "chg": 0, "pct": 0, "prev": 0}

@st.cache_data(ttl=120)
def get_hist(sym, period, interval):
    try:
        df = yf.download(sym, period=period, interval=interval, progress=False, auto_adjust=True)
        df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
        return df
    except:
        return pd.DataFrame()

@st.cache_data(ttl=300)
def get_info(sym):
    try:
        return yf.Ticker(sym).info
    except:
        return {}

@st.cache_data(ttl=300)
def get_news(api_key, query="Indian stock market NSE BSE"):
    if not api_key:
        return []
    try:
        r = requests.get("https://newsapi.org/v2/everything", params={
            "q": query, "apiKey": api_key, "sortBy": "publishedAt",
            "pageSize": 15, "language": "en",
        }, timeout=8)
        data = r.json()
        return data.get("articles", []) if data.get("status") == "ok" else []
    except:
        return []

def time_ago(s):
    if not s: return ""
    try:
        dt = datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
        d  = int((datetime.utcnow() - dt).total_seconds())
        if d < 3600:  return f"{d//60}m ago"
        if d < 86400: return f"{d//3600}h ago"
        return f"{d//86400}d ago"
    except:
        return ""

def fmt_inr(v):
    if v is None: return "—"
    try:
        v = float(v)
        if v >= 1e12: return f"₹{v/1e12:.2f}T"
        if v >= 1e9:  return f"₹{v/1e9:.2f}B"
        if v >= 1e7:  return f"₹{v/1e7:.2f}Cr"
        if v >= 1e5:  return f"₹{v/1e5:.2f}L"
        return f"₹{v:,.0f}"
    except:
        return "—"

def pct_color(p):
    return "up" if p >= 0 else "down"

def pct_arrow(p):
    return "▲" if p >= 0 else "▼"


# ─── CHART BUILDER ────────────────────────────────────────────────────────────
def build_chart(df, sym, chart_type, is_positive):
    if df.empty:
        return go.Figure()

    color_up   = "#22c55e"
    color_down = "#ef4444"
    line_color = color_up if is_positive else color_down
    fill_color = "rgba(34,197,94,0.08)" if is_positive else "rgba(239,68,68,0.08)"

    fig = go.Figure()

    if chart_type == "Candle" and all(c in df.columns for c in ["Open","High","Low","Close"]):
        fig.add_trace(go.Candlestick(
            x=df.index, open=df["Open"], high=df["High"],
            low=df["Low"], close=df["Close"],
            increasing_line_color=color_up, decreasing_line_color=color_down,
            increasing_fillcolor=color_up+"44", decreasing_fillcolor=color_down+"44",
            line_width=1,
        ))
    elif chart_type == "Area" and "Close" in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df["Close"], mode="lines",
            line=dict(color=line_color, width=1.5, shape="spline"),
            fill="tozeroy", fillcolor=fill_color,
        ))
    else:
        if "Close" in df.columns:
            fig.add_trace(go.Scatter(
                x=df.index, y=df["Close"], mode="lines",
                line=dict(color=line_color, width=1.5),
            ))

    # Volume bars at bottom
    if "Volume" in df.columns:
        vol_colors = [color_up if c >= o else color_down
                      for c, o in zip(df.get("Close", df.index), df.get("Open", df.index))]
        fig.add_trace(go.Bar(
            x=df.index, y=df["Volume"], marker_color=vol_colors,
            opacity=0.25, yaxis="y2", name="Vol",
        ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=8, t=0, b=0),
        height=300,
        showlegend=False,
        xaxis=dict(
            showgrid=False, zeroline=False,
            tickfont=dict(family="DM Mono", size=10, color="#4b5563"),
            rangeslider=dict(visible=False),
            color="#4b5563",
        ),
        yaxis=dict(
            showgrid=True, gridcolor="#1e2130", zeroline=False,
            tickfont=dict(family="DM Mono", size=10, color="#4b5563"),
            side="right", color="#4b5563",
        ),
        yaxis2=dict(overlaying="y", side="left", showgrid=False, showticklabels=False),
        hovermode="x unified",
        hoverlabel=dict(bgcolor="#161820", font=dict(family="DM Mono", size=11, color="#e5e7eb"), bordercolor="#1e2130"),
    )
    return fig


def build_mini_chart(df, is_positive):
    if df.empty or "Close" not in df.columns:
        return go.Figure()
    color = "#22c55e" if is_positive else "#ef4444"
    fill  = "rgba(34,197,94,0.1)" if is_positive else "rgba(239,68,68,0.1)"
    fig = go.Figure(go.Scatter(
        x=df.index, y=df["Close"], mode="lines",
        line=dict(color=color, width=1.5, shape="spline"),
        fill="tozeroy", fillcolor=fill,
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0,r=0,t=0,b=0), height=50, showlegend=False,
        xaxis=dict(visible=False), yaxis=dict(visible=False),
    )
    return fig


# ─── FETCH CURRENT DATA ───────────────────────────────────────────────────────
idx_quotes   = {i["sym"]: get_quote(i["sym"]) for i in INDICES}
wl_quotes    = {w["sym"]: get_quote(w["sym"])  for w in st.session_state.watchlist}
period_key   = st.session_state.period
hist_period, hist_interval = PERIODS[period_key]
hist_df      = get_hist(st.session_state.selected_sym, hist_period, hist_interval)
selected_q   = get_quote(st.session_state.selected_sym)
info         = get_info(st.session_state.selected_sym)
is_positive  = selected_q["pct"] >= 0


# ─── TOP BAR ──────────────────────────────────────────────────────────────────
idx_chips = ""
for i in INDICES:
    q   = idx_quotes.get(i["sym"], {})
    p   = q.get("price", 0)
    pct = q.get("pct", 0)
    cls = "up" if pct >= 0 else "down"
    arr = "▲" if pct >= 0 else "▼"
    idx_chips += f"""
    <div class="index-chip">
      <span class="ic-name">{i['name']}</span>
      <span class="ic-val">{p:,.2f}</span>
      <span class="ic-chg {cls}">{arr} {abs(pct):.2f}%</span>
    </div>"""

now_str = datetime.now().strftime("%d %b %Y  %H:%M IST")
st.markdown(f"""
<div class="topbar">
  <span class="logo">◈ BHARAT</span>
  {idx_chips}
  <span class="topbar-time">{now_str}</span>
  <span class="topbar-live">● LIVE</span>
</div>
""", unsafe_allow_html=True)


# ─── THREE-COLUMN LAYOUT ──────────────────────────────────────────────────────
left_col, center_col, right_col = st.columns([240/1200, 680/1200, 280/1200])


# ══════════════════════════════════════════════════════════════════════════════
# LEFT PANEL
# ══════════════════════════════════════════════════════════════════════════════
with left_col:
    # ── Add to watchlist ──
    with st.expander("+ Add to Watchlist", expanded=False):
        new_sym  = st.text_input("Symbol (e.g. BAJFINANCE.NS)", key="add_input", label_visibility="collapsed", placeholder="e.g. BAJFINANCE.NS")
        new_name = st.text_input("Display name", key="add_name", label_visibility="collapsed", placeholder="Display name")
        if st.button("Add", use_container_width=True):
            if new_sym:
                st.session_state.watchlist.append({"sym": new_sym.upper(), "name": new_name or new_sym})
                st.rerun()

    # ── Watchlist ──
    st.markdown('<div class="panel-title">WATCHLIST</div>', unsafe_allow_html=True)
    for w in st.session_state.watchlist:
        q   = wl_quotes.get(w["sym"], {})
        p   = q.get("price", 0)
        pct = q.get("pct", 0)
        chg = q.get("chg", 0)
        cls = "up" if pct >= 0 else "down"
        arr = "▲" if pct >= 0 else "▼"
        is_active = w["sym"] == st.session_state.selected_sym
        active_cls = "active" if is_active else ""
        if st.button(f"{w['sym'].replace('.NS','').replace('.BO','')}  ₹{p:,.2f}  {arr}{abs(pct):.2f}%", key=f"wl_{w['sym']}", use_container_width=True):
            st.session_state.selected_sym  = w["sym"]
            st.session_state.selected_name = w["name"]
            st.rerun()

    st.markdown("<hr style='border:none;border-top:1px solid #1e2130;margin:8px 0'>", unsafe_allow_html=True)

    # ── News API Key input ──
    st.markdown('<div class="panel-title">NEWS API KEY</div>', unsafe_allow_html=True)
    nk = st.text_input("NewsAPI Key", type="password", placeholder="newsapi.org key…", label_visibility="collapsed", key="napi")
    if nk: st.session_state.news_key = nk

    # ── News feed ──
    st.markdown('<div class="panel-title">TOP NEWS</div>', unsafe_allow_html=True)
    articles = get_news(st.session_state.news_key, f"India NSE BSE {st.session_state.selected_name}")
    if articles:
        for a in articles[:10]:
            src  = a.get("source", {}).get("name", "")[:20]
            head = (a.get("title") or "")[:70]
            pub  = a.get("publishedAt", "")
            url  = a.get("url", "#")
            st.markdown(f"""
            <div class="news-item" onclick="window.open('{url}','_blank')">
              <div class="news-src">{src}</div>
              <div class="news-head">{head}…</div>
              <div class="news-time">{time_ago(pub)}</div>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div style="padding:10px 14px;font-size:0.68rem;color:#374151;font-family:DM Mono,monospace;">Enter NewsAPI key for live news</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# CENTER PANEL
# ══════════════════════════════════════════════════════════════════════════════
with center_col:
    chg_cls = "up" if is_positive else "down"
    arr = "▲" if is_positive else "▼"

    # ── Stock header ──
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown(f"""
        <div class="stock-title">{st.session_state.selected_name}</div>
        <div class="stock-sub">{st.session_state.selected_sym} · NSE/BSE</div>
        """, unsafe_allow_html=True)
    with c2:
        p = selected_q.get("price", 0)
        pct = selected_q.get("pct", 0)
        chg = selected_q.get("chg", 0)
        st.markdown(f"""
        <div style="text-align:right">
          <div class="stock-price">₹{p:,.2f}</div>
          <div class="stock-chg-big {chg_cls}">{arr} ₹{abs(chg):,.2f} ({abs(pct):.2f}%)</div>
        </div>""", unsafe_allow_html=True)

    # ── Period + chart type selector ──
    pc = st.columns(len(PERIODS) + 3)
    for i, (label, _) in enumerate(PERIODS.items()):
        if pc[i].button(label, key=f"p_{label}", use_container_width=True,
                        type="primary" if st.session_state.period == label else "secondary"):
            st.session_state.period = label
            st.rerun()
    for j, ct in enumerate(CHART_TYPES):
        if pc[len(PERIODS)+j].button(ct, key=f"ct_{ct}", use_container_width=True,
                                     type="primary" if st.session_state.chart_type == ct else "secondary"):
            st.session_state.chart_type = ct
            st.rerun()

    # ── Chart ──
    fig = build_chart(hist_df, st.session_state.selected_sym, st.session_state.chart_type, is_positive)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # ── Key metrics ──
    st.markdown('<div class="section-hdr">// KEY METRICS</div>', unsafe_allow_html=True)
    prev = selected_q.get("prev", 0)
    high52 = info.get("fiftyTwoWeekHigh")
    low52  = info.get("fiftyTwoWeekLow")
    mktcap = info.get("marketCap")
    pe     = info.get("trailingPE")
    eps    = info.get("trailingEps")
    div_yld= info.get("dividendYield")
    vol    = info.get("volume")
    avg_vol= info.get("averageVolume")
    beta   = info.get("beta")

    metrics = [
        ("Prev Close",  f"₹{prev:,.2f}"       if prev else "—"),
        ("52W High",    f"₹{high52:,.2f}"      if high52 else "—"),
        ("52W Low",     f"₹{low52:,.2f}"       if low52 else "—"),
        ("Market Cap",  fmt_inr(mktcap)),
        ("P/E Ratio",   f"{pe:.2f}"            if pe else "—"),
        ("EPS",         f"₹{eps:.2f}"          if eps else "—"),
        ("Div Yield",   f"{div_yld*100:.2f}%"  if div_yld else "—"),
        ("Volume",      f"{vol:,}"             if vol else "—"),
        ("Avg Volume",  f"{avg_vol:,}"         if avg_vol else "—"),
        ("Beta",        f"{beta:.2f}"          if beta else "—"),
        ("Day High",    f"₹{info.get('dayHigh',0):,.2f}" if info.get("dayHigh") else "—"),
        ("Day Low",     f"₹{info.get('dayLow',0):,.2f}"  if info.get("dayLow") else "—"),
    ]
    cols_m = st.columns(4)
    for i, (lbl, val) in enumerate(metrics):
        with cols_m[i % 4]:
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-label">{lbl}</div>
              <div class="metric-value">{val}</div>
            </div>""", unsafe_allow_html=True)

    # ── Sector charts (mini sparklines) ──
    st.markdown('<br><div class="section-hdr">// SECTOR PERFORMANCE</div>', unsafe_allow_html=True)
    sec_cols = st.columns(4)
    for i, s in enumerate(SECTOR_ETFS):
        q = get_quote(s["sym"])
        pct_s = q.get("pct", 0)
        with sec_cols[i % 4]:
            color = "#22c55e" if pct_s >= 0 else "#ef4444"
            arr_s = "▲" if pct_s >= 0 else "▼"
            st.markdown(f"""
            <div class="metric-card" style="text-align:center">
              <div class="metric-label">{s['name']}</div>
              <div class="metric-value" style="color:{color};font-size:0.8rem">{arr_s} {abs(pct_s):.2f}%</div>
            </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# RIGHT PANEL
# ══════════════════════════════════════════════════════════════════════════════
with right_col:
    # ── Tabs ──
    tabs = ["Gainers", "Losers", "Indices", "Commodities", "MCX"]
    tab_html = '<div class="tab-bar">'
    for t in tabs:
        active = "active" if st.session_state.right_tab == t else ""
        tab_html += f'<span class="tab {active}" id="tab_{t}">{t}</span>'
    tab_html += '</div>'
    st.markdown(tab_html, unsafe_allow_html=True)

    tab_cols = st.columns(len(tabs))
    for i, t in enumerate(tabs):
        if tab_cols[i].button(t, key=f"rtab_{t}", use_container_width=True,
                              type="primary" if st.session_state.right_tab == t else "secondary"):
            st.session_state.right_tab = t
            st.rerun()

    active_tab = st.session_state.right_tab

    # ── Gainers / Losers ──
    if active_tab in ("Gainers", "Losers"):
        nifty50 = [
            "RELIANCE.NS","TCS.NS","HDFCBANK.NS","INFY.NS","ICICIBANK.NS","HINDUNILVR.NS",
            "ITC.NS","SBIN.NS","BHARTIARTL.NS","KOTAKBANK.NS","LT.NS","AXISBANK.NS",
            "ASIANPAINT.NS","MARUTI.NS","TITAN.NS","WIPRO.NS","BAJFINANCE.NS","NESTLEIND.NS",
            "ULTRACEMCO.NS","TECHM.NS",
        ]
        rows = []
        for sym in nifty50[:15]:
            q = get_quote(sym)
            rows.append({"sym": sym.replace(".NS",""), "price": q["price"], "pct": q["pct"]})

        rows.sort(key=lambda x: x["pct"], reverse=(active_tab == "Gainers"))
        for r in rows[:12]:
            cls = "up" if r["pct"] >= 0 else "down"
            arr_r = "▲" if r["pct"] >= 0 else "▼"
            if st.button(f"{r['sym']}  ₹{r['price']:,.2f}  {arr_r}{abs(r['pct']):.2f}%",
                         key=f"gr_{r['sym']}", use_container_width=True):
                st.session_state.selected_sym  = r["sym"] + ".NS"
                st.session_state.selected_name = r["sym"]
                st.rerun()

    # ── Indices ──
    elif active_tab == "Indices":
        all_indices = INDICES + [
            {"sym": "^CNXSMALLCAP", "name": "NIFTY Smallcap"},
            {"sym": "^CNXINFRA",    "name": "NIFTY Infra"},
            {"sym": "^CNXPHARMA",   "name": "NIFTY Pharma"},
            {"sym": "^CNXFMCG",     "name": "NIFTY FMCG"},
            {"sym": "^CNXAUTO",     "name": "NIFTY Auto"},
            {"sym": "^CNXREALTY",   "name": "NIFTY Realty"},
        ]
        for idx in all_indices:
            q   = get_quote(idx["sym"])
            p   = q.get("price", 0)
            pct = q.get("pct", 0)
            cls = "up" if pct >= 0 else "down"
            arr_i = "▲" if pct >= 0 else "▼"
            if st.button(f"{idx['name']}  {p:,.2f}  {arr_i}{abs(pct):.2f}%",
                         key=f"idx_{idx['sym']}", use_container_width=True):
                st.session_state.selected_sym  = idx["sym"]
                st.session_state.selected_name = idx["name"]
                st.rerun()

    # ── Commodities ──
    elif active_tab == "Commodities":
        for c in COMMODITIES:
            q   = get_quote(c["sym"])
            p   = q.get("price", 0)
            pct = q.get("pct", 0)
            cls = "up" if pct >= 0 else "down"
            arr_c = "▲" if pct >= 0 else "▼"
            sym_lbl = c["sym"].replace("=F","").replace("=X","")
            if st.button(f"{c['name']}  {p:,.2f}  {arr_c}{abs(pct):.2f}%",
                         key=f"com_{c['sym']}", use_container_width=True):
                st.session_state.selected_sym  = c["sym"]
                st.session_state.selected_name = c["name"]
                st.rerun()

    # ── MCX ──
    elif active_tab == "MCX":
        for m in MCX_STOCKS:
            q   = get_quote(m["sym"])
            p   = q.get("price", 0)
            pct = q.get("pct", 0)
            arr_m = "▲" if pct >= 0 else "▼"
            if st.button(f"{m['name']}  ₹{p:,.2f}  {arr_m}{abs(pct):.2f}%",
                         key=f"mcx_{m['sym']}", use_container_width=True):
                st.session_state.selected_sym  = m["sym"]
                st.session_state.selected_name = m["name"]
                st.rerun()

    # ── Selected stock mini chart in right panel ──
    st.markdown("<hr style='border:none;border-top:1px solid #1e2130;margin:10px 0'>", unsafe_allow_html=True)
    st.markdown(f'<div style="font-family:DM Mono,monospace;font-size:0.6rem;color:#4b5563;padding:4px 0;text-transform:uppercase;letter-spacing:0.1em">{st.session_state.selected_sym.replace(".NS","").replace(".BO","")} · 1M TREND</div>', unsafe_allow_html=True)
    mini_df = get_hist(st.session_state.selected_sym, "1mo", "1d")
    mini_fig = build_mini_chart(mini_df, is_positive)
    st.plotly_chart(mini_fig, use_container_width=True, config={"displayModeBar": False})

    # ── Refresh button ──
    st.markdown("<hr style='border:none;border-top:1px solid #1e2130;margin:8px 0'>", unsafe_allow_html=True)
    if st.button("⟳  Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    st.markdown('<div style="font-family:DM Mono,monospace;font-size:0.58rem;color:#374151;text-align:center;padding:6px 0;">Data via Yahoo Finance · 2min cache</div>', unsafe_allow_html=True)
