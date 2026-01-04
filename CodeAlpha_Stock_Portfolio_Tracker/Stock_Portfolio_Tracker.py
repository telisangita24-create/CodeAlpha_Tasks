"""
Advanced Stock Portfolio Tracker with Streamlit
Features: GUI, Real-time Prices, Performance Tracking, Visualization
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Tuple
import time

# Page configuration
st.set_page_config(
    page_title="Stock Portfolio Tracker",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #F8F9FA;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1E3A8A;
        margin-bottom: 1rem;
    }
    .stock-card {
        background-color: #FFFFFF;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 0.5rem;
    }
    .positive {
        color: #10B981;
        font-weight: bold;
    }
    .negative {
        color: #EF4444;
        font-weight: bold;
    }
    .section-header {
        font-size: 1.5rem;
        color: #374151;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #E5E7EB;
    }
</style>
""", unsafe_allow_html=True)

class PortfolioTracker:
    """Main portfolio tracking class"""
    
    def __init__(self):
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'portfolio' not in st.session_state:
            st.session_state.portfolio = {}
        if 'transactions' not in st.session_state:
            st.session_state.transactions = []
        if 'portfolio_history' not in st.session_state:
            st.session_state.portfolio_history = {}
        if 'selected_period' not in st.session_state:
            st.session_state.selected_period = '1mo'
    
    def get_default_stocks(self) -> Dict[str, float]:
        """Get default stock prices (fallback if API fails)"""
        return {
            "AAPL": 180.50,
            "TSLA": 250.75,
            "GOOGL": 135.20,
            "MSFT": 330.42,
            "AMZN": 145.60,
            "META": 350.25,
            "NVDA": 450.30,
            "JPM": 155.80,
            "V": 240.90,
            "WMT": 165.35
        }
    
    def get_current_price(self, symbol: str) -> float:
        """Get current stock price using yfinance"""
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period='1d')
            if not hist.empty:
                return float(hist['Close'].iloc[-1])
        except:
            pass
        
        # Fallback to default prices
        default_prices = self.get_default_stocks()
        return default_prices.get(symbol, 0.0)
    
    def get_historical_data(self, symbol: str, period: str = '1mo') -> pd.DataFrame:
        """Get historical stock data"""
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period=period)
            return hist
        except:
            return pd.DataFrame()
    
    def add_stock(self, symbol: str, quantity: float, price: float = None):
        """Add stock to portfolio"""
        symbol = symbol.upper().strip()
        
        if price is None:
            price = self.get_current_price(symbol)
        
        if symbol in st.session_state.portfolio:
            # Update existing holding
            old_qty = st.session_state.portfolio[symbol]['quantity']
            old_avg = st.session_state.portfolio[symbol]['avg_price']
            
            new_qty = old_qty + quantity
            new_avg = ((old_qty * old_avg) + (quantity * price)) / new_qty
            
            st.session_state.portfolio[symbol]['quantity'] = new_qty
            st.session_state.portfolio[symbol]['avg_price'] = new_avg
        else:
            # Add new holding
            st.session_state.portfolio[symbol] = {
                'quantity': quantity,
                'avg_price': price,
                'purchase_date': datetime.now().strftime("%Y-%m-%d")
            }
        
        # Record transaction
        transaction = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'symbol': symbol,
            'action': 'BUY',
            'quantity': quantity,
            'price': price,
            'total': quantity * price
        }
        st.session_state.transactions.append(transaction)
    
    def remove_stock(self, symbol: str, quantity: float):
        """Remove stock from portfolio"""
        symbol = symbol.upper().strip()
        
        if symbol not in st.session_state.portfolio:
            st.error(f"{symbol} not found in portfolio")
            return False
        
        current_qty = st.session_state.portfolio[symbol]['quantity']
        
        if quantity > current_qty:
            st.error(f"Cannot remove more than current quantity ({current_qty})")
            return False
        
        current_price = self.get_current_price(symbol)
        
        # Update portfolio
        if quantity == current_qty:
            del st.session_state.portfolio[symbol]
        else:
            st.session_state.portfolio[symbol]['quantity'] -= quantity
        
        # Record transaction
        transaction = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'symbol': symbol,
            'action': 'SELL',
            'quantity': quantity,
            'price': current_price,
            'total': quantity * current_price
        }
        st.session_state.transactions.append(transaction)
        
        return True
    
    def calculate_portfolio_value(self) -> Dict:
        """Calculate current portfolio value and metrics"""
        portfolio = st.session_state.portfolio
        
        if not portfolio:
            return {
                'total_value': 0.0,
                'total_cost': 0.0,
                'total_gain': 0.0,
                'gain_percentage': 0.0,
                'holdings': []
            }
        
        holdings = []
        total_cost = 0.0
        total_current_value = 0.0
        
        for symbol, data in portfolio.items():
            current_price = self.get_current_price(symbol)
            quantity = data['quantity']
            avg_price = data['avg_price']
            
            current_value = quantity * current_price
            cost_basis = quantity * avg_price
            gain = current_value - cost_basis
            gain_percentage = (gain / cost_basis * 100) if cost_basis > 0 else 0
            
            holdings.append({
                'symbol': symbol,
                'quantity': quantity,
                'avg_price': avg_price,
                'current_price': current_price,
                'cost_basis': cost_basis,
                'current_value': current_value,
                'gain': gain,
                'gain_percentage': gain_percentage
            })
            
            total_cost += cost_basis
            total_current_value += current_value
        
        total_gain = total_current_value - total_cost
        total_gain_percentage = (total_gain / total_cost * 100) if total_cost > 0 else 0
        
        return {
            'total_value': total_current_value,
            'total_cost': total_cost,
            'total_gain': total_gain,
            'gain_percentage': total_gain_percentage,
            'holdings': holdings
        }
    
    def track_portfolio_history(self):
        """Track portfolio value over time"""
        portfolio_value = self.calculate_portfolio_value()
        today = datetime.now().strftime("%Y-%m-%d")
        
        if today not in st.session_state.portfolio_history:
            st.session_state.portfolio_history[today] = portfolio_value['total_value']
    
    def get_portfolio_history_chart(self, period_days: int = 30):
        """Generate portfolio history chart"""
        if len(st.session_state.portfolio_history) < 2:
            return None
        
        # Simulate historical data for demonstration
        # In production, you'd store actual daily values
        dates = pd.date_range(end=datetime.now(), periods=period_days, freq='D')
        values = []
        
        current_value = self.calculate_portfolio_value()['total_value']
        
        # Generate realistic looking historical data
        for i in range(period_days):
            # Simulate some random variation
            variation = np.random.normal(0, 0.02)  # 2% daily variation
            value = current_value * (1 + variation * (period_days - i) / period_days)
            values.append(max(value, 0))
        
        # Reverse to get increasing timeline
        values = values[::-1]
        
        return pd.DataFrame({
            'Date': dates,
            'Portfolio Value': values
        })
    
    def export_portfolio(self, format_type: str = 'csv'):
        """Export portfolio data"""
        portfolio_data = self.calculate_portfolio_value()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format_type == 'csv':
            # Export holdings to CSV
            holdings_df = pd.DataFrame(portfolio_data['holdings'])
            filename = f"portfolio_export_{timestamp}.csv"
            holdings_df.to_csv(filename, index=False)
            return filename
        else:
            # Export to JSON
            export_data = {
                'export_date': timestamp,
                'portfolio_summary': {
                    'total_value': portfolio_data['total_value'],
                    'total_cost': portfolio_data['total_cost'],
                    'total_gain': portfolio_data['total_gain'],
                    'gain_percentage': portfolio_data['gain_percentage']
                },
                'holdings': portfolio_data['holdings'],
                'transactions': st.session_state.transactions
            }
            filename = f"portfolio_export_{timestamp}.json"
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2)
            return filename
    
    def display_portfolio_metrics(self, portfolio_data: Dict):
        """Display portfolio metrics in Streamlit"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total Portfolio Value",
                value=f"${portfolio_data['total_value']:,.2f}",
                delta=f"{portfolio_data['gain_percentage']:.2f}%"
            )
        
        with col2:
            st.metric(
                label="Total Cost Basis",
                value=f"${portfolio_data['total_cost']:,.2f}"
            )
        
        with col3:
            delta_color = "normal" if portfolio_data['total_gain'] >= 0 else "inverse"
            st.metric(
                label="Total Gain/Loss",
                value=f"${portfolio_data['total_gain']:,.2f}",
                delta_color=delta_color
            )
        
        with col4:
            st.metric(
                label="Number of Holdings",
                value=len(portfolio_data['holdings'])
            )
    
    def render_sidebar(self):
        """Render sidebar controls"""
        with st.sidebar:
            st.markdown("## 📊 Portfolio Controls")
            
            # Add Stock Form
            st.markdown("### Add Stock")
            with st.form("add_stock_form"):
                symbol = st.text_input("Stock Symbol", placeholder="AAPL").upper()
                quantity = st.number_input("Quantity", min_value=0.1, value=1.0, step=0.1)
                price = st.number_input("Purchase Price (optional)", min_value=0.00, value=0.00, step=0.01)
                
                if st.form_submit_button("Add to Portfolio", width='stretch'):
                    if symbol:
                        self.add_stock(symbol, quantity, price if price > 0 else None)
                        st.success(f"Added {quantity} shares of {symbol}")
                        st.rerun()
            
            st.divider()
            
            # Remove Stock Form
            st.markdown("### Remove Stock")
            if st.session_state.portfolio:
                symbols = list(st.session_state.portfolio.keys())
                selected_symbol = st.selectbox("Select Stock", symbols)
                selected_qty = st.number_input(
                    "Quantity to Remove",
                    min_value=0.1,
                    max_value=st.session_state.portfolio[selected_symbol]['quantity'],
                    value=1.0,
                    step=0.1,
                    key="remove_qty"
                )
                
                if st.button("Remove from Portfolio", width='stretch'):
                    if self.remove_stock(selected_symbol, selected_qty):
                        st.success(f"Removed {selected_qty} shares of {selected_symbol}")
                        st.rerun()
            else:
                st.info("No stocks in portfolio")
            
            st.divider()
            
            # Export Options
            st.markdown("### Export Data")
            export_format = st.selectbox("Format", ["CSV", "JSON"])
            if st.button("Export Portfolio", width='stretch'):
                filename = self.export_portfolio(export_format.lower())
                st.success(f"Exported to {filename}")
                
                with open(filename, "rb") as file:
                    st.download_button(
                        label="Download File",
                        data=file,
                        file_name=filename,
                        mime="text/csv" if export_format == "CSV" else "application/json"
                    )
            
            st.divider()
            
            # Clear Portfolio
            if st.button("Clear Portfolio", type="secondary", width='stretch'):
                st.session_state.portfolio = {}
                st.session_state.transactions = []
                st.rerun()
            
            # Display Info
            st.markdown("---")
            st.markdown("**💡 Tips:**")
            st.markdown("""
            - Use stock symbols (e.g., AAPL, TSLA)
            - Prices update automatically
            - Track performance over time
            - Export data for analysis
            """)

def main():
    """Main Streamlit application"""
    # Initialize tracker
    tracker = PortfolioTracker()
    
    # Header
    st.markdown("<h1 class='main-header'>📈 Advanced Stock Portfolio Tracker</h1>", unsafe_allow_html=True)
    
    # Sidebar
    tracker.render_sidebar()
    
    # Main content area
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Portfolio Overview", "📈 Performance", "📋 Holdings", "🔄 Transactions"])
    
    # Track history
    tracker.track_portfolio_history()
    
    # Calculate portfolio data
    portfolio_data = tracker.calculate_portfolio_value()
    
    with tab1:
        # Portfolio Metrics
        st.markdown("<h2 class='section-header'>Portfolio Summary</h2>", unsafe_allow_html=True)
        tracker.display_portfolio_metrics(portfolio_data)
        
        # Performance Chart
        st.markdown("<h2 class='section-header'>Portfolio Performance</h2>", unsafe_allow_html=True)
        
        # Period selector
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            period = st.selectbox(
                "Time Period",
                ["1W", "1M", "3M", "6M", "1Y", "All"],
                index=1,
                key="period_selector"
            )
        
        # Generate and display chart
        history_data = tracker.get_portfolio_history_chart(
            period_days={
                "1W": 7,
                "1M": 30,
                "3M": 90,
                "6M": 180,
                "1Y": 365,
                "All": 365
            }[period]
        )
        
        if history_data is not None:
            fig = go.Figure()
            
            # Add portfolio value line
            fig.add_trace(go.Scatter(
                x=history_data['Date'],
                y=history_data['Portfolio Value'],
                mode='lines',
                name='Portfolio Value',
                line=dict(color='#1E3A8A', width=3),
                fill='tozeroy',
                fillcolor='rgba(30, 58, 138, 0.1)'
            ))
            
            # Update layout
            fig.update_layout(
                title=f"Portfolio Value Over Time ({period})",
                xaxis_title="Date",
                yaxis_title="Portfolio Value ($)",
                hovermode='x unified',
                template='plotly_white',
                height=400
            )
            
            st.plotly_chart(fig,width='stretch')
        else:
            st.info("Add stocks to your portfolio to see performance charts.")
        
        # Allocation Pie Chart
        if portfolio_data['holdings']:
            st.markdown("<h2 class='section-header'>Portfolio Allocation</h2>", unsafe_allow_html=True)
            
            holdings_df = pd.DataFrame(portfolio_data['holdings'])
            fig = go.Figure(data=[go.Pie(
                labels=holdings_df['symbol'],
                values=holdings_df['current_value'],
                hole=.3,
                textinfo='label+percent',
                marker=dict(colors=px.colors.qualitative.Set3)
            )])
            
            fig.update_layout(
                title="Portfolio Allocation by Stock",
                height=400
            )
            
            st.plotly_chart(fig, width='stretch')
    
    with tab2:
        st.markdown("<h2 class='section-header'>Detailed Performance Analysis</h2>", unsafe_allow_html=True)
        
        if portfolio_data['holdings']:
            # Create performance comparison
            perf_df = pd.DataFrame(portfolio_data['holdings'])
            
            # Sort by current value
            perf_df = perf_df.sort_values('current_value', ascending=False)
            
            # Display performance metrics for each stock
            for _, row in perf_df.iterrows():
                col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 2])
                
                with col1:
                    st.markdown(f"**{row['symbol']}**")
                
                with col2:
                    st.markdown(f"**Qty:** {row['quantity']:.2f}")
                
                with col3:
                    st.markdown(f"**Price:** ${row['current_price']:.2f}")
                
                with col4:
                    st.markdown(f"**Value:** ${row['current_value']:.2f}")
                
                with col5:
                    gain_class = "positive" if row['gain'] >= 0 else "negative"
                    st.markdown(f"<span class='{gain_class}'>Gain: ${row['gain']:.2f} ({row['gain_percentage']:.2f}%)</span>", unsafe_allow_html=True)
                
                # Mini progress bar for allocation
                allocation = (row['current_value'] / portfolio_data['total_value']) * 100
                st.progress(allocation / 100, text=f"Allocation: {allocation:.1f}%")
            
            # Performance Comparison Chart
            st.markdown("<h3 class='section-header'>Performance Comparison</h3>", unsafe_allow_html=True)
            
            fig = go.Figure()
            
            # Add bars for gain/loss
            colors = ['#10B981' if x >= 0 else '#EF4444' for x in perf_df['gain_percentage']]
            
            fig.add_trace(go.Bar(
                x=perf_df['symbol'],
                y=perf_df['gain_percentage'],
                name='Gain %',
                marker_color=colors,
                text=perf_df['gain_percentage'].apply(lambda x: f'{x:.1f}%'),
                textposition='auto'
            ))
            
            fig.update_layout(
                title="Gain/Loss Percentage by Stock",
                xaxis_title="Stock Symbol",
                yaxis_title="Gain/Loss (%)",
                height=400
            )
            
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("No stocks in portfolio. Add some stocks to see performance analysis.")
    
    with tab3:
        st.markdown("<h2 class='section-header'>Current Holdings</h2>", unsafe_allow_html=True)
        
        if portfolio_data['holdings']:
            # Display holdings in a nice format
            holdings_df = pd.DataFrame(portfolio_data['holdings'])
            
            # Format the DataFrame for display
            display_df = holdings_df.copy()
            display_df['avg_price'] = display_df['avg_price'].apply(lambda x: f"${x:.2f}")
            display_df['current_price'] = display_df['current_price'].apply(lambda x: f"${x:.2f}")
            display_df['cost_basis'] = display_df['cost_basis'].apply(lambda x: f"${x:,.2f}")
            display_df['current_value'] = display_df['current_value'].apply(lambda x: f"${x:,.2f}")
            display_df['gain'] = display_df['gain'].apply(lambda x: f"${x:,.2f}")
            display_df['gain_percentage'] = display_df['gain_percentage'].apply(lambda x: f"{x:.2f}%")
            
            # Rename columns for better display
            display_df = display_df.rename(columns={
                'symbol': 'Symbol',
                'quantity': 'Quantity',
                'avg_price': 'Avg Price',
                'current_price': 'Current Price',
                'cost_basis': 'Cost Basis',
                'current_value': 'Current Value',
                'gain': 'Gain/Loss',
                'gain_percentage': 'Gain %'
            })
            
            # Display as table
            st.dataframe(
                display_df,
                width='stretch',
                hide_index=True
            )
            
            # Summary statistics
            st.markdown("<h3 class='section-header'>Holding Statistics</h3>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Holdings", len(holdings_df))
            with col2:
                st.metric("Avg Gain %", f"{holdings_df['gain_percentage'].mean():.2f}%")
            with col3:
                best_performer = holdings_df.loc[holdings_df['gain_percentage'].idxmax()]
                st.metric("Best Performer", f"{best_performer['symbol']} ({best_performer['gain_percentage']:.2f}%)")
        else:
            st.info("No holdings in portfolio. Use the sidebar to add stocks.")
    
    with tab4:
        st.markdown("<h2 class='section-header'>Transaction History</h2>", unsafe_allow_html=True)
        
        if st.session_state.transactions:
            # Convert to DataFrame for display
            trans_df = pd.DataFrame(st.session_state.transactions)
            
            # Format for display
            display_trans = trans_df.copy()
            display_trans['price'] = display_trans['price'].apply(lambda x: f"${x:.2f}")
            display_trans['total'] = display_trans['total'].apply(lambda x: f"${x:.2f}")
            
            # Add color coding for action
            def color_action(action):
                return 'color: green' if action == 'BUY' else 'color: red'
            
            # Display styled DataFrame
            st.dataframe(
                display_trans.style.applymap(color_action, subset=['action']),
                width='stretch',
                hide_index=True
            )
            
            # Transaction summary
            st.markdown("<h3 class='section-header'>Transaction Summary</h3>", unsafe_allow_html=True)
            
            buy_count = sum(1 for t in st.session_state.transactions if t['action'] == 'BUY')
            sell_count = sum(1 for t in st.session_state.transactions if t['action'] == 'SELL')
            total_volume = sum(t['total'] for t in st.session_state.transactions)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Transactions", len(st.session_state.transactions))
            with col2:
                st.metric("Buy/Sell Ratio", f"{buy_count}/{sell_count}")
            with col3:
                st.metric("Total Volume", f"${total_volume:,.2f}")
        else:
            st.info("No transactions yet. Buy or sell stocks to see transaction history.")
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            """
            <div style='text-align: center; color: #6B7280; font-size: 0.9rem;'>
                <p>📊 Portfolio data updates automatically | 💰 Prices are for demonstration purposes</p>
                <p>⚠️ This is a demo application. Not financial advice.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()