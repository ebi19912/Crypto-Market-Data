
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# List of valid trading pairs
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
resolutions = ['1', '5', '15', '30', '60', '180', '240', '360', '720', 'D', '2D', '3D']

def get_global_stats():
    url = 'https://api.nobitex.ir/market/global-stats'
    response = requests.post(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_historical_data(symbol, resolution, from_timestamp, to_timestamp):
    url = f'https://api.nobitex.ir/market/udf/history?symbol={symbol}&resolution={resolution}&from={from_timestamp}&to={to_timestamp}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

st.title("📊 Nobitex Market Stats and Charts")

st.sidebar.header("🎛️ Choose Parameters")
selected_symbol = st.sidebar.selectbox("🔹 Select Pair", symbols, index=symbols.index("BTCUSDT"))
selected_resolution = st.sidebar.selectbox("⏳ Select Resolution", resolutions)
start_date = st.sidebar.date_input("📅 Start Date", value=datetime.now() - timedelta(days=90))
end_date = st.sidebar.date_input("📅 End Date", value=datetime.now())
chart_type = st.sidebar.radio("📈 Chart Type", ['Candlestick', 'Line'])

start_timestamp = int(datetime.combine(start_date, datetime.min.time()).timestamp())
end_timestamp = int(datetime.combine(end_date, datetime.max.time()).timestamp())

global_stats = get_global_stats()
if global_stats and global_stats.get('status') == 'ok':
    st.subheader("🌍 Global Prices")
    base_currency = selected_symbol[:3].lower()
    if base_currency in global_stats:
        for source, data in global_stats[base_currency].items():
            st.markdown(f"**{source.upper()}**: {data['price']:,} IRR")
    else:
        st.warning(f"No global stats found for {base_currency.upper()}.")
else:
    st.error("❌ Failed to fetch global stats.")

historical_data = get_historical_data(selected_symbol, selected_resolution, start_timestamp, end_timestamp)
if historical_data and historical_data.get('s') == 'ok':
    df = pd.DataFrame({
        'time': pd.to_datetime(historical_data['t'], unit='s'),
        'open': historical_data['o'],
        'high': historical_data['h'],
        'low': historical_data['l'],
        'close': historical_data['c'],
        'volume': historical_data['v']
    })

    st.subheader("📄 Data Table")
    st.dataframe(df.tail(10))

    fig = go.Figure()
    if chart_type == 'Candlestick':
        fig.add_trace(go.Candlestick(
            x=df['time'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name="Price"
        ))
    else:
        fig.add_trace(go.Scatter(
            x=df['time'],
            y=df['close'],
            mode='lines',
            name="Close Price"
        ))

    fig.add_trace(go.Bar(
        x=df['time'],
        y=df['volume'],
        name="Volume",
        marker=dict(color='lightblue'),
        yaxis='y2',
        opacity=0.4
    ))

    fig.update_layout(
        title=f"📉 {selected_symbol} Price Chart",
        xaxis_title="Date",
        yaxis_title="Price",
        yaxis2=dict(
            title="Volume",
            overlaying='y',
            side='right',
            showgrid=False
        ),
        legend=dict(orientation="h")
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("⚠️ No data found or failed to fetch data for selected range.")
