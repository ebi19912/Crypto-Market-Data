"""
=============================================================================
Nobitex Cryptocurrency Market Data Dashboard (English Edition)
=============================================================================
This application is built with Streamlit and communicates directly with
Nobitex's public market REST APIs. It allows users to track global benchmark
prices, examine historical OHLCV (Open, High, Low, Close, Volume) candlestick
data for over 200 crypto trading pairs, and visualize interactive charts.
=============================================================================
"""

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# =============================================================================
# 1. Streamlit Application Page Configuration
# =============================================================================
st.set_page_config(
    page_title="Nobitex Crypto Market Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# 2. List of Supported Cryptocurrency Trading Pairs on Nobitex
# =============================================================================
# Contains trading pairs quoted in both USDT and IRT (Iranian Rial Token).
symbols = [
    'BTCIRT', 'ETHIRT', 'LTCIRT', 'USDTIRT', 'XRPIRT', 'BCHIRT', 'BNBIRT',
    'EOSIRT', 'XLMIRT', 'ETCIRT', 'TRXIRT', 'DOGEIRT', 'UNIIRT', 'DAIIRT',
    'LINKIRT', 'DOTIRT', 'AAVEIRT', 'ADAIRT', 'SHIBIRT', 'FTMIRT', 'MATICIRT',
    'AXSIRT', 'MANAIRT', 'SANDIRT', 'AVAXIRT', 'MKRIRT', 'GMTIRT', 'USDCIRT',
    'BTCUSDT', 'ETHUSDT', 'LTCUSDT', 'XRPUSDT', 'BCHUSDT', 'BNBUSDT', 'EOSUSDT',
    'XLMUSDT', 'ETCUSDT', 'TRXUSDT', 'PMNUSDT', 'DOGEUSDT', 'UNIUSDT', 'DAIUSDT',
    'LINKUSDT', 'DOTUSDT', 'AAVEUSDT', 'ADAUSDT', 'SHIBUSDT', 'FTMUSDT', 'MATICUSDT',
    'AXSUSDT', 'MANAUSDT', 'SANDUSDT', 'AVAXUSDT', 'MKRUSDT', 'GMTUSDT', 'USDCUSDT',
    'CHZIRT', 'GRTIRT', 'CRVIRT', 'BANDUSDT', 'COMPUSDT', 'EGLDIRT', 'HBARUSDT',
    'GALIRT', 'HBARIRT', 'WBTCUSDT', 'IMXIRT', 'WBTCIRT', 'ONEIRT', 'GLMUSDT',
    'ENSIRT', '1M_BTTIRT', 'SUSHIIRT', 'LDOIRT', 'ATOMUSDT', 'ZROIRT', 'STORJIRT',
    'ANTIRT', 'AEVOUSDT', '100K_FLOKIIRT', 'RSRUSDT', 'API3USDT', 'GLMIRT',
    'XMRIRT', 'ENSUSDT', 'OMIRT', 'RDNTIRT', 'MAGICUSDT', 'TIRT', 'ATOMIRT',
    'NOTIRT', 'CVXIRT', 'XTZIRT', 'FILIRT', 'UMAIRT', '1B_BABYDOGEIRT', 'BANDIRT',
    'SSVIRT', 'DAOIRT', 'BLURIRT', 'ONEUSDT', 'EGALAUSDT', 'GMXIRT', 'XTZUSDT',
    'FLOWUSDT', 'GALUSDT', 'WIRT', 'CVCUSDT', 'NMRUSDT', 'SKLIRT', 'SNTIRT',
    'BATUSDT', 'TRBUSDT', 'NMRIRT', 'RDNTUSDT', 'API3IRT', 'CVCIRT', 'WLDIRT',
    'YFIUSDT', 'SOLIRT', 'TUSDT', 'QNTUSDT', 'IMXUSDT', 'AEVOIRT', 'GMXUSDT',
    'ETHFIUSDT', 'QNTIRT', 'GRTUSDT', 'WLDUSDT', 'FETIRT', 'AGIXIRT', 'NOTUSDT',
    'LPTIRT', 'SLPIRT', 'MEMEUSDT', 'SOLUSDT', 'BALUSDT', 'DAOUSDT', 'COMPIRT',
    'MEMEIRT', 'TONIRT', 'BATIRT', 'SNXIRT', 'TRBIRT', '1INCHUSDT', 'OMUSDT',
    'RSRIRT', 'RNDRIRT', 'SLPUSDT', 'SSVUSDT', 'RNDRUSDT', 'AGLDIRT', 'NEARUSDT',
    'WOOUSDT', 'YFIIRT', 'MDTIRT', 'CRVUSDT', 'MDTUSDT', 'EGLDUSDT', 'LRCIRT',
    'LPTUSDT', 'BICOUSDT', '1M_PEPEIRT', 'BICOIRT', 'MAGICIRT', 'ETHFIIRT',
    'ANTUSDT', '1INCHIRT', 'APEUSDT', '1M_NFTIRT', 'ARBIRT', 'LRCUSDT', 'WUSDT',
    'BLURUSDT', 'CELRUSDT', 'DYDXIRT', 'CVXUSDT', 'BALIRT', 'TONUSDT', '100K_FLOKIUSDT',
    'JSTUSDT', 'ZROUSDT', 'ARBUSDT', 'APTIRT', '1M_NFTUSDT', 'CELRIRT', 'UMAUSDT',
    'SKLUSDT', 'ZRXUSDT', 'AGLDUSDT', 'ALGOIRT', 'NEARIRT', 'APTUSDT', 'ZRXIRT',
    'SUSHIUSDT', 'FETUSDT', 'ALGOUSDT', '1M_PEPEUSDT', 'MASKIRT', 'EGALAIRT',
    'FLOWIRT', '1B_BABYDOGEUSDT', 'MASKUSDT', '1M_BTTUSDT', 'STORJUSDT', 'XMRUSDT',
    'OMGIRT', 'SNTUSDT', 'APEIRT', 'FILUSDT', 'ENJUSDT', 'OMGUSDT', 'WOOIRT',
    'CHZUSDT', 'ENJIRT', 'DYDXUSDT', 'AGIXUSDT', 'JSTIRT', 'LDOUSDT', 'SNXUSDT'
]

# =============================================================================
# 3. Standard Candlestick Timeframe Resolutions (TradingView UDF)
# =============================================================================
# Integer values represent minutes: 1, 5, 15, 30, 60 (1h), 180 (3h), 240 (4h),
# 360 (6h), 720 (12h). 'D', '2D', '3D' denote daily aggregations.
resolutions = ['1', '5', '15', '30', '60', '180', '240', '360', '720', 'D', '2D', '3D']

# =============================================================================
# 4. API Communication Functions
# =============================================================================

@st.cache_data(ttl=60)
def get_global_stats():
    """
    Fetches the latest global benchmark prices for major cryptocurrencies from Nobitex API.

    Returns:
        dict or None: JSON response dictionary containing global currency statistics,
                      or None if request fails.
    """
    url = 'https://api.nobitex.ir/market/global-stats'
    try:
        response = requests.post(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.RequestException:
        return None


@st.cache_data(ttl=300)
def get_historical_data(symbol: str, resolution: str, from_timestamp: int, to_timestamp: int):
    """
    Retrieves historical OHLCV candlestick data for a trading pair via the Nobitex UDF API.

    Args:
        symbol (str): Market trading pair symbol (e.g., 'BTCUSDT', 'ETHIRT').
        resolution (str): Candlestick resolution (e.g., '60', 'D').
        from_timestamp (int): Start date as Unix Epoch timestamp in seconds.
        to_timestamp (int): End date as Unix Epoch timestamp in seconds.

    Returns:
        dict or None: UDF formatted dictionary containing:
            - 't': List of candle open timestamps (seconds)
            - 'o': List of opening prices
            - 'h': List of high prices
            - 'l': List of low prices
            - 'c': List of closing prices
            - 'v': List of traded volume
            - 's': Status string ('ok' or 'no_data')
    """
    url = (
        f'https://api.nobitex.ir/market/udf/history'
        f'?symbol={symbol}&resolution={resolution}&from={from_timestamp}&to={to_timestamp}'
    )
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.RequestException:
        return None


# =============================================================================
# 5. User Interface & Parameter Controls (Sidebar)
# =============================================================================

# Main Page Heading
st.title("📊 Nobitex Crypto Market Intelligence Dashboard")
st.caption("Real-time global benchmarks, historical OHLCV data & interactive technical charting")

# Sidebar Configuration
st.sidebar.header("🎛️ Market Parameters")

# Symbol Selection
default_idx = symbols.index("BTCUSDT") if "BTCUSDT" in symbols else 0
selected_symbol = st.sidebar.selectbox("🔹 Select Trading Pair", symbols, index=default_idx)

# Resolution Selection
default_res_idx = resolutions.index("D") if "D" in resolutions else 0
selected_resolution = st.sidebar.selectbox("⏳ Timeframe Resolution", resolutions, index=default_res_idx)

# Date Range Selection
default_start_date = datetime.now() - timedelta(days=90)
start_date = st.sidebar.date_input("📅 Start Date", value=default_start_date)
end_date = st.sidebar.date_input("📅 End Date", value=datetime.now())

# Chart Type Radio
chart_type = st.sidebar.radio("📈 Chart Type", ['Candlestick', 'Line'])

# Date Validation
if start_date > end_date:
    st.sidebar.error("⚠️ Start date must be before or equal to End date.")

# Convert date inputs to Unix timestamps in seconds
start_timestamp = int(datetime.combine(start_date, datetime.min.time()).timestamp())
end_timestamp = int(datetime.combine(end_date, datetime.max.time()).timestamp())

# =============================================================================
# 6. Global Price Benchmarks Section
# =============================================================================
global_stats = get_global_stats()
if global_stats and global_stats.get('status') == 'ok':
    st.subheader("🌍 Global Benchmark Prices")
    
    # Extract base asset symbol (e.g., 'btc' from 'BTCUSDT' or 'BTCIRT')
    base_currency = selected_symbol.replace('IRT', '').replace('USDT', '').lower()
    
    if base_currency in global_stats:
        cols = st.columns(len(global_stats[base_currency]))
        for idx, (source, data) in enumerate(global_stats[base_currency].items()):
            with cols[idx]:
                price_val = data.get('price', 0)
                st.metric(label=f"Source: {source.upper()}", value=f"{price_val:,.0f} IRR")
    else:
        st.info(f"ℹ️ No global benchmark statistics available for asset `{base_currency.upper()}`.")
else:
    st.warning("⚠️ Global market statistics are currently unavailable.")

st.divider()

# =============================================================================
# 7. Historical OHLCV Data Processing & Plotly Visualization
# =============================================================================
historical_data = get_historical_data(selected_symbol, selected_resolution, start_timestamp, end_timestamp)

if historical_data and historical_data.get('s') == 'ok' and len(historical_data.get('t', [])) > 0:
    # Convert JSON arrays into Pandas DataFrame
    df = pd.DataFrame({
        'time': pd.to_datetime(historical_data['t'], unit='s'),
        'open': historical_data['o'],
        'high': historical_data['h'],
        'low': historical_data['l'],
        'close': historical_data['c'],
        'volume': historical_data['v']
    })

    # Summary metric cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Latest Close", f"{df['close'].iloc[-1]:,}")
    with col2:
        st.metric("Period High", f"{df['high'].max():,}")
    with col3:
        st.metric("Period Low", f"{df['low'].min():,}")
    with col4:
        st.metric("Total Volume", f"{df['volume'].sum():,.2f}")

    # Build Interactive Plotly Figure
    fig = go.Figure()

    # Price Trace (Candlestick or Line)
    if chart_type == 'Candlestick':
        fig.add_trace(go.Candlestick(
            x=df['time'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name="Price (OHLC)",
            increasing_line_color='#26a69a',
            decreasing_line_color='#ef5350'
        ))
    else:
        fig.add_trace(go.Scatter(
            x=df['time'],
            y=df['close'],
            mode='lines',
            name="Closing Price",
            line=dict(color='#2962FF', width=2)
        ))

    # Volume Sub-chart on Secondary Y-Axis
    fig.add_trace(go.Bar(
        x=df['time'],
        y=df['volume'],
        name="Trading Volume",
        marker=dict(color='rgba(100, 181, 246, 0.4)'),
        yaxis='y2'
    ))

    # Dual-axis Layout Customization
    fig.update_layout(
        title=dict(
            text=f"📉 {selected_symbol} Technical Chart (Timeframe: {selected_resolution})",
            x=0.5,
            xanchor='center'
        ),
        xaxis_title="Date & Time",
        yaxis_title="Price",
        yaxis2=dict(
            title="Volume",
            overlaying='y',
            side='right',
            showgrid=False
        ),
        xaxis_rangeslider_visible=False,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_white",
        hovermode="x unified",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    # Render Plotly Chart
    st.plotly_chart(fig, use_container_width=True)

    # Data Table View
    st.subheader("📄 Recent Candlestick Records")
    st.dataframe(
        df.tail(10).style.format({
            'open': '{:,.2f}',
            'high': '{:,.2f}',
            'low': '{:,.2f}',
            'close': '{:,.2f}',
            'volume': '{:,.4f}'
        }),
        use_container_width=True
    )

else:
    st.warning("⚠️ No historical data found for the selected symbol and timeframe, or failed to connect.")
