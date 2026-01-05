### Advanced Stock Portfolio Tracker
📈 Smart, simple, and analytics-driven stock portfolio manager built with Python and Streamlit.

A lightweight Streamlit app to track holdings, view real-time prices (via yFinance), analyze portfolio performance, and export data. Designed for personal use, learning, and small-scale portfolio monitoring.

### Features
Real-time price lookup using yFinance
Auto-calculated portfolio metrics: total value, cost basis, gain/loss (amount and %)
Add / remove (sell) holdings; supports partial sells and automatic average-price recalculation
Transaction history with timestamps and color-coded BUY/SELL entries
Interactive charts:
Portfolio value over selectable ranges (1W, 1M, 3M, 6M, 1Y, All)
Allocation donut chart
Gain/Loss comparison bar chart
Export portfolio and transactions to CSV or JSON
Clean Streamlit layout with Plotly charts and custom styling

### Tech stack
Frontend: Streamlit
Language: Python 3.8+
Charts: Plotly (graph_objects / express)
Data: yFinance
Data handling: pandas, numpy
Session storage: Streamlit session_state

### Requirements
Python 3.8 or higher
Internet connection (for fetching live prices)
Install dependencies:

pip install -r requirements.txt

### Quick start
- Add a new holding: enter symbol (e.g., AAPL), quantity, optional purchase price → Add to Portfolio
- Remove / Sell: choose a holding and quantity → Remove from Portfolio (partial sells supported)
- View charts: switch between Overview, Performance, Holdings, Transactions tabs in the sidebar
- Export: choose CSV or JSON and click Download

### License & Acknowledgements
This project is free for personal and educational use.
Acknowledgements:
- Streamlit — UI framework
- yFinance — market data
- Plotly — visualizations
- pandas / NumPy — data processing
