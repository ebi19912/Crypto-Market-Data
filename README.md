Project Overview: Crypto-Market-Data is a specialized engine developed to build comprehensive historical datasets for cryptocurrency markets. It systematically retrieves every single candlestick (OHLCV) from the inception of each market up to the current date, providing a rich foundation for algorithmic trading and market analysis.

Technical Scope:

Extensive Market Coverage: Supports over 200 trading pairs, including major assets (BTC, ETH, BNB) against both USDT and IRT (Iranian Rial Token).

Multi-Resolution Support: Capable of fetching data in various timeframes: 1m, 5m, 15m, 30m, 60m, 180m, 240m, 360m, 720m, Daily, 2-Day, and 3-Day resolutions.

Global & Local Markets: Covers international pairs like SOLUSDT and MATICUSDT, as well as localized pairs like BTCIRT and SHIBIRT.

Technical Features:

Full Historical Retrieval: Unlike standard tools, this harvester is designed to fetch data from the very first day a symbol was listed.

Multi-Language Support: Includes both English (market_app_en.py) and Persian (market_app.py) versions of the application for broader usability.

Data Integrity: Implements robust logic to handle API rate limits and ensure continuous data flow during large-scale harvesting tasks.

Technical Stack:

Language: Python (100%).

Core Components: RESTful API Integration, Time-Series Data Management, and Asynchronous Requests.
