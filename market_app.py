"""
=============================================================================
برنامه تحلیل و نمایش داده‌های بازار ارزهای دیجیتال نوبیتکس (نسخه فارسی)
Crypto Market Data Viewer - Persian Edition
=============================================================================
این برنامه با استفاده از پلتفرم Streamlit و وب‌سرویس‌های (API) عمومی صرافی نوبیتکس
توسعه یافته است. کاربر می‌تواند جفت‌ارزهای مختلف (ریالی و تتری)، بازه‌های زمانی،
و نوع نمودار را انتخاب کرده و آمار لحظه‌ای و نمودار تکنیکال قیمت و حجم را مشاهده نماید.
=============================================================================
"""

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# =============================================================================
# ۱. پیکربندی تنظیمات اولیه صفحه در استریم‌لیت (Streamlit Page Configuration)
# =============================================================================
st.set_page_config(
    page_title="داشبورد داده‌های بازار نوبیتکس",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# ۲. لیست جفت‌ارزهای معتبر و پشتیبانی‌شده در صرافی نوبیتکس (Trading Pairs)
# =============================================================================
# این لیست شامل جفت‌ارزهای مبتنی بر تومان (IRT) و تتر (USDT) می‌باشد.
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
# ۳. بازه‌های زمانی استاندارد کندل‌ها (TradingView UDF Resolutions)
# =============================================================================
# مقادیر عددی بر حسب دقیقه هستند: ۱، ۵، ۱۵، ۳۰، ۶۰ (یک ساعت)، ۱۸۰ (۳ ساعت)،
# ۲۴۰ (۴ ساعت)، ۳۶۰ (۶ ساعت)، ۷۲۰ (۱۲ ساعت) و D (روزانه)، 2D (۲ روزه)، 3D (۳ روزه)
resolutions = ['1', '5', '15', '30', '60', '180', '240', '360', '720', 'D', '2D', '3D']

# =============================================================================
# ۴. توابع دریافت داده از API نوبیتکس (API Fetching Functions)
# =============================================================================

@st.cache_data(ttl=60)
def get_global_stats():
    """
    دریافت آخرین آمار و نرخ‌های جهانی رمزارزها از نوبیتکس.
    
    این تابع داده‌های قیمت جهانی را از اندپوینت `global-stats` دریافت می‌کند.
    برای بهینه‌سازی و کاهش درخواست‌های تکراری، نتایج به مدت ۶۰ ثانیه کَش (Cache) می‌شوند.

    خروجی:
        dict یا None: دیکشنری شامل وضعیت و قیمت رمزارزها در صورت موفقیت، یا None در صورت بروز خطا.
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
    دریافت داده‌های تاریخی قیمت (OHLCV) برای جفت‌ارز و بازه زمانی مشخص بر اساس استاندارد UDF.

    ورودی‌ها:
        symbol (str): نماد معاملاتی (مثلاً 'BTCIRT' یا 'ETHUSDT').
        resolution (str): تایم‌فریم کندل‌ها (مثلاً '60', 'D').
        from_timestamp (int): زمان شروع به فرمت Unix Timestamp (بر حسب ثانیه).
        to_timestamp (int): زمان پایان به فرمت Unix Timestamp (بر حسب ثانیه).

    خروجی:
        dict یا None: ساختار داده استاندارد UDF شامل:
            - 't': آرایه زمان باز شدن کندل‌ها (Unix Timestamp)
            - 'o': آرایه قیمت باز شدن (Open)
            - 'h': آرایه بالاترین قیمت (High)
            - 'l': آرایه پایین‌ترین قیمت (Low)
            - 'c': آرایه قیمت بسته شدن (Close)
            - 'v': آرایه حجم معاملات (Volume)
            - 's': وضعیت پاسخ ('ok' یا 'no_data')
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
# ۵. رابط کاربری داشبورد (UI Layout & Controls)
# =============================================================================

# عنوان اصلی صفحه
st.title("📊 آمار و نمودار تعاملی بازار نوبیتکس")
st.caption("سامانه تحلیل داده‌های تاریخی و قیمت‌های جهانی رمزارزها | بر پایه API صرافی نوبیتکس")

# منوی کناری (Sidebar) برای دریافت ورودی‌ها از کاربر
st.sidebar.header("🎛️ تنظیمات و فیلترها")

# انتخاب جفت‌ارز
default_index = symbols.index("BTCIRT") if "BTCIRT" in symbols else 0
selected_symbol = st.sidebar.selectbox("🔹 انتخاب جفت‌ارز", symbols, index=default_index)

# انتخاب تایم‌فریم (رزولوشن)
selected_resolution = st.sidebar.selectbox("⏳ انتخاب بازه زمانی (تایم‌فریم)", resolutions, index=resolutions.index("D") if "D" in resolutions else 0)

# انتخاب بازه زمانی (تاریخ شروع و پایان)
default_start = datetime.now() - timedelta(days=90)
start_date = st.sidebar.date_input("📅 تاریخ شروع", value=default_start)
end_date = st.sidebar.date_input("📅 تاریخ پایان", value=datetime.now())

# نوع نمودار قیمت
chart_type = st.sidebar.radio("📈 نوع نمودار قیمت", ['کندل‌استیک', 'خطی'])

# اعتبارسنجی بازه تاریخی
if start_date > end_date:
    st.sidebar.error("⚠️ تاریخ شروع نمی‌تواند بعد از تاریخ پایان باشد!")

# تبدیل تاریخ‌های انتخابی کاربر به Unix Timestamp (بر حسب ثانیه)
start_timestamp = int(datetime.combine(start_date, datetime.min.time()).timestamp())
end_timestamp = int(datetime.combine(end_date, datetime.max.time()).timestamp())

# =============================================================================
# ۶. بخش نمایش قیمت‌ها و آمار جهانی (Global Stats Section)
# =============================================================================
global_stats = get_global_stats()
if global_stats and global_stats.get('status') == 'ok':
    st.subheader("🌍 قیمت‌های مرجع جهانی")
    
    # استخراج رمزارز پایه بر اساس نماد (مثلاً btc از BTCIRT یا BTCUSDT)
    base_currency = selected_symbol.replace('IRT', '').replace('USDT', '').lower()
    
    if base_currency in global_stats:
        cols = st.columns(len(global_stats[base_currency]))
        for idx, (source, data) in enumerate(global_stats[base_currency].items()):
            with cols[idx]:
                price_val = data.get('price', 0)
                st.metric(label=f"منبع: {source.upper()}", value=f"{price_val:,.0f} تومان")
    else:
        st.info(f"ℹ️ آمار قیمت مرجع جهانی برای نماد {base_currency.upper()} در دسترس نیست.")
else:
    st.warning("⚠️ امکان دریافت لحظه‌ای آمار قیمت جهانی وجود ندارد.")

st.divider()

# =============================================================================
# ۷. دریافت، پردازش و رسم داده‌های کندل‌استیک تاریخی (Historical Data Processing)
# =============================================================================
historical_data = get_historical_data(selected_symbol, selected_resolution, start_timestamp, end_timestamp)

if historical_data and historical_data.get('s') == 'ok' and len(historical_data.get('t', [])) > 0:
    # تبدیل داده‌های بازگشتی JSON به دیتافریم پانداس
    df = pd.DataFrame({
        'time': pd.to_datetime(historical_data['t'], unit='s'),
        'open': historical_data['o'],
        'high': historical_data['h'],
        'low': historical_data['l'],
        'close': historical_data['c'],
        'volume': historical_data['v']
    })

    # نمایش اطلاعات آماری خلاصه
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("آخرین قیمت ثبت‌شده", f"{df['close'].iloc[-1]:,}")
    with col2:
        st.metric("بالاترین قیمت در بازه", f"{df['high'].max():,}")
    with col3:
        st.metric("پایین‌ترین قیمت در بازه", f"{df['low'].min():,}")
    with col4:
        st.metric("مجموع حجم معاملات", f"{df['volume'].sum():,.2f}")

    # رسم نمودار ترکیبی تعاملی با کتابخانه Plotly
    fig = go.Figure()

    # رسم نمودار قیمت بر اساس نوع انتخاب شده (کندل‌استیک یا خطی)
    if chart_type == 'کندل‌استیک':
        fig.add_trace(go.Candlestick(
            x=df['time'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name="قیمت (کندل)",
            increasing_line_color='#26a69a',
            decreasing_line_color='#ef5350'
        ))
    else:
        fig.add_trace(go.Scatter(
            x=df['time'],
            y=df['close'],
            mode='lines',
            name="قیمت پایانی",
            line=dict(color='#2962FF', width=2)
        ))

    # اضافه کردن نمودار ستونی حجم معاملات روی محور عمودی دوم (y2)
    fig.add_trace(go.Bar(
        x=df['time'],
        y=df['volume'],
        name="حجم معاملات",
        marker=dict(color='rgba(100, 181, 246, 0.4)'),
        yaxis='y2'
    ))

    # پیکربندی استایل، عناوین و محورهای دوگانه نمودار
    fig.update_layout(
        title=dict(
            text=f"📉 نمودار تکنیکال {selected_symbol} (تایم‌فریم {selected_resolution})",
            x=0.5,
            xanchor='center'
        ),
        xaxis_title="تاریخ و زمان",
        yaxis_title="قیمت",
        yaxis2=dict(
            title="حجم معاملات",
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

    # نمایش نمودار داخل استریم‌لیت
    st.plotly_chart(fig, use_container_width=True)

    # نمایش جدول ۱۰ کندل آخر
    st.subheader("📄 جدول آخرین داده‌های دریافتی")
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
    st.warning("⚠️ داده‌ای برای بازه زمانی و نماد انتخاب‌شده یافت نشد یا ارتباط با سرور با خطا مواجه شده است.")
