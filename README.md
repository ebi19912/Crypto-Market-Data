# 📊 Crypto Market Data & Charting Engine
### داشبورد جامع تحلیل و مصورسازی داده‌های بازار رمزارز نوبیتکس

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit App](https://img.shields.io/badge/Framework-Streamlit-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Visualization-Plotly-3F4F75.svg?logo=plotly&logoColor=white)](https://plotly.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Nobitex API](https://img.shields.io/badge/API-Nobitex%20Public%20API-orange.svg)](https://nobitex.ir/)

---

## 🌐 زبان‌ها / Languages
- [فارسی (Persian)](#-بخش-فارسی)
- [English](#-english-section)

---

<a name="-بخش-فارسی"></a>
# 🇮🇷 بخش فارسی

## 📋 معرفی پروژه
**Crypto-Market-Data** یک پلتفرم تعاملی و ابزار تحلیل داده‌های بازار رمزارزها بر بستر وب است که با استفاده از پایتون، فریم‌ورک **Streamlit**، کتابخانه مصورسازی **Plotly** و اتصال مستقیم به وب‌سرویس‌های عمومی صرافی **نوبیتکس (Nobitex)** پیاده‌سازی شده است.

این سامانه به تحلیل‌گران، تریدرها و توسعه‌دهندگان الگوریتم‌های معاملاتی امکان می‌دهد تا:
1. داده‌های قیمتی تاریخی (کندل‌استیک‌های OHLCV) را از ابتدای فهرست شدن تا لحظه جاری با تایم‌فریم‌های گوناگون دریافت و تحلیل نمایند.
2. قیمت‌های مرجع جهانی رمزارزها را به صورت آنی مقایسه کنند.
3. نمودارهای تکنیکال تعاملی با محور دوگانه (Dual-Axis) برای قیمت و حجم معاملات را رسم و پیمایش کنند.

---

## ✨ ویژگی‌های کلیدی
- **پوشش بیش از ۲۰۰ جفت‌ارز معاملاتی**: پشتیبانی کامل از بازارهای ریالی/تومانی (`IRT`) و تتری (`USDT`) شامل BTC, ETH, SOL, TON, SHIB, DOGE و...
- **پشتیبانی از چندین تایم‌فریم (رزولوشن)**: دریافت داده در تایم‌فریم‌های ۱، ۵، ۱۵، ۳۰، ۶۰ (۱ ساعت)، ۱۸۰ (۳ ساعت)، ۲۴۰ (۴ ساعت)، ۳۶۰ (۶ ساعت)، ۷۲۰ (۱۲ ساعت) و روزانه (D, 2D, 3D).
- **نمودارهای تعاملی پیشرفته**: رسم نمودارهای شمعی ژاپنی (Candlestick) و نمودار خطی همراه با اندیکاتور حجم معاملات روی محور مجزا.
- **آمار و مظنه‌های جهانی**: دریافت قیمت‌های مرجع بین‌المللی با اندپوینت `global-stats`.
- **بهینه‌سازی با کَشینگ (Caching)**: استفاده از مکانیسم کش هوشمند استریم‌لیت جهت کاهش ترافیک شبکه و افزایش چشمگیر سرعت بارگذاری.
- **دو زبانه بودن (Bilingual)**: ارائه نسخه کامل فارسی (`market_app.py`) و انگلیسی (`market_app_en.py`).

---

## 🗂️ ساختار پروژه
```text
Crypto-Market-Data/
├── market_app.py         # برنامه تحت وب با رابط کاربری و توضیحات فارسی
├── market_app_en.py      # برنامه تحت وب با رابط کاربری و توضیحات انگلیسی
├── requirements.txt      # لیست پیش‌نیازها و پکیج‌های پایتون
├── .gitignore            # فایل‌های نادیده‌گرفته‌شده توسط گیت
└── README.md             # مستندات کامل پروژه به دو زبان فارسی و انگلیسی
```

---

## 🚀 راهنمای نصب و راه‌اندازی

### ۱. کلون کردن مخزن
```bash
git clone https://github.com/ebi19912/Crypto-Market-Data.git
cd Crypto-Market-Data
```

### ۲. ساخت و فعال‌سازی محیط مجازی (Virtual Environment)
```bash
# ویندوز (PowerShell / CMD)
python -m venv venv
.\venv\Scripts\activate

# لینوکس / مک
python3 -m venv venv
source venv/bin/activate
```

### ۳. نصب پیش‌نیازها
```bash
pip install -r requirements.txt
```

### ۴. اجرای برنامه
- **اجرای نسخه فارسی:**
```bash
streamlit run market_app.py
```
- **اجرای نسخه انگلیسی:**
```bash
streamlit run market_app_en.py
```
سپس مرورگر خود را باز کرده و به آدرس `http://localhost:8501` مراجعه کنید.

---

## 🔌 وب‌سرویس‌های استفاده‌شده (API Endpoints)
این برنامه مستقیماً با APIهای عمومی نوبیتکس ارتباط برقرار می‌کند و نیاز به کلید دسترسی (API Key) ندارد:
- **داده‌های کندل‌استیک (UDF):**
  `GET https://api.nobitex.ir/market/udf/history?symbol={symbol}&resolution={resolution}&from={from}&to={to}`
- **آمار و قیمت‌های جهانی:**
  `POST https://api.nobitex.ir/market/global-stats`

---
---

<a name="-english-section"></a>
# 🇬🇧 English Section

## 📋 Project Overview
**Crypto-Market-Data** is an interactive cryptocurrency market analysis and visualization suite powered by **Python**, **Streamlit**, **Plotly**, and direct integration with **Nobitex's Public REST APIs**.

It enables quantitative analysts, traders, and crypto enthusiasts to systematically fetch historical OHLCV (Open, High, Low, Close, Volume) candlestick records, examine global benchmark valuations, and interactively explore financial charts.

---

## ✨ Key Features
- **200+ Trading Pairs**: Full coverage across both USDT and IRT (Iranian Rial) quoted markets (e.g., BTC, ETH, SOL, XRP, DOGE, ADA).
- **Multi-Resolution Timeframes**: Supports 1m, 5m, 15m, 30m, 60m (1h), 180m (3h), 240m (4h), 360m (6h), 720m (12h), 1D, 2D, and 3D resolutions.
- **Rich Interactive Visualizations**: Dual-axis Plotly charts featuring Candlestick / Line price action coupled with trading volume histograms.
- **Global Valuation Benchmarks**: Real-time cross-referencing of international cryptocurrency price indices.
- **Smart Data Caching**: In-memory response caching via Streamlit's `@st.cache_data` to ensure low latency and prevent API throttling.
- **Dual Language Support**: Standalone implementations in both Persian (`market_app.py`) and English (`market_app_en.py`).

---

## 🗂️ Project Structure
```text
Crypto-Market-Data/
├── market_app.py         # Persian UI Streamlit Application
├── market_app_en.py      # English UI Streamlit Application
├── requirements.txt      # Python dependencies specification
├── .gitignore            # Git exclusion rules
└── README.md             # Comprehensive bilingual project documentation
```

---

## 🚀 Installation & Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/ebi19912/Crypto-Market-Data.git
cd Crypto-Market-Data
```

### 2. Create & Activate a Virtual Environment
```bash
# Windows (PowerShell / CMD)
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
- **To launch the Persian Dashboard:**
```bash
streamlit run market_app.py
```
- **To launch the English Dashboard:**
```bash
streamlit run market_app_en.py
```
Open your browser and navigate to `http://localhost:8501`.

---

## 🛠️ Tech Stack & Dependencies
- **Core Language**: Python 3.9+
- **Web UI & Dashboard**: Streamlit
- **Data Manipulation**: Pandas
- **Charting & Graphics**: Plotly (Plotly Graph Objects)
- **HTTP Client**: Requests

---

## 🔗 Integrated Endpoints
The platform utilizes public endpoints that do not require API authentication:
1. **TradingView UDF Historical Candlesticks**:
   `GET https://api.nobitex.ir/market/udf/history?symbol={symbol}&resolution={resolution}&from={from}&to={to}`
2. **Global Benchmark Statistics**:
   `POST https://api.nobitex.ir/market/global-stats`

---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page or submit a Pull Request.

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
