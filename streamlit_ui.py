# import streamlit as st
# import requests
#
# st.set_page_config(page_title="Strategy Signal Dashboard", page_icon="📈")
# st.title("📈 Strategy Signal Dashboard")
#
# symbol = st.text_input("Enter Symbol (e.g., EURUSD)", "EURUSD")
# market = st.selectbox("Select Market", ["forex", "nse"], index=0)
# interval = st.selectbox("Select Interval", ["1m", "5m", "15m", "1h", "1d"], index=3)
# auto_trade = st.checkbox("Enable Auto Trade?", value=False)
#
# strategy_type = st.radio("Select Strategy Type", ["Predefined", "Custom"])
#
# if strategy_type == "Predefined":
#     # Fetch predefined strategies from API
#     try:
#         res = requests.get("http://127.0.0.1:8080/strategy/predefined_List")
#         strategies = res.json()
#         strategy_names = [s["name"] for s in strategies]
#         selected_strategy = st.selectbox("Choose Predefined Strategy", strategy_names)
#     except Exception as e:
#         st.error(f"Failed to load predefined strategies: {e}")
#
# else:
#     custom_name = st.text_input("Custom Strategy Name", "my_custom_macd")
#     indicator = st.selectbox("Indicator", ["macd", "rsi", "sma"])
#     operator = st.selectbox("Operator", [">", "<", ">=", "<=", "=="])
#     value = st.number_input("Value", step=0.01)
#
# if st.button("Apply Strategy"):
#     try:
#         if strategy_type == "Predefined":
#             payload = {
#                 "symbol": symbol,
#                 "strategy_name": selected_strategy,
#                 "market": market,
#                 "interval": interval,
#                 "auto_trade": auto_trade
#             }
#             url = "http://127.0.0.1:8080/strategy/apply_predefined"
#         else:
#             payload = {
#                 "symbol": symbol,
#                 "strategy": {
#                     "name": custom_name,
#                     "conditions": [
#                         {
#                             "indicator": indicator,
#                             "operator": operator,
#                             "value": value
#                         }
#                     ]
#                 },
#                 "market": market,
#                 "interval": interval,
#                 "auto_trade": auto_trade
#             }
#             url = "http://127.0.0.1:8080/strategy/apply_custom"
#
#         res = requests.post(url, json=payload)
#         if res.status_code == 200:
#             st.success("✅ Strategy applied successfully!")
#             st.json(res.json())
#         else:
#             st.error(f"❌ Failed to apply strategy: {res.text}")
#
#     except Exception as e:
#         st.error(f"Exception occurred: {e}")




import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import pandas_ta as ta
import time
import datetime


# Fetch tick data from API


def fetch_tick_data(symbol, market, interval):
    url = f"http://localhost:8080/completedata/{symbol}?market={market}"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            df = pd.DataFrame(res.json())
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
            df.set_index('timestamp', inplace=True)
            return df
        else:
            st.error("No tick data found or server error.")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()


# Create Candlestick chart
def plot_candlestick(df):
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                                         open=df['open'], high=df['high'], low=df['low'], close=df['close'],
                                         name="Candlestick")])
    fig.update_layout(title="Candlestick Chart", xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)


# Apply Strategy Function
def apply_strategy(df, strategy_type, interval):
    if strategy_type == 'RSI Oversold':
        # RSI Indicator Strategy
        df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
        signal = (df['rsi'] < 30).iloc[-1]  # Buy signal when RSI is less than 30
        action = 'Buy' if signal else 'Hold'
    else:
        # Default strategy can be extended
        action = 'Hold'

    return action


# Backtesting Function (basic example)
def backtest_strategy(df, strategy_type):
    df['action'] = 'Hold'
    if strategy_type == 'RSI Oversold':
        df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
        df.loc[df['rsi'] < 30, 'action'] = 'Buy'

    buy_signals = df[df['action'] == 'Buy']
    win_count = 0
    loss_count = 0
    total_profit = 0

    for index, row in buy_signals.iterrows():
        buy_price = row['close']
        sell_price = df.loc[index:].iloc[-1]['close']
        profit = sell_price - buy_price
        if profit > 0:
            win_count += 1
        else:
            loss_count += 1
        total_profit += profit

    st.write(f"Backtesting Results: Win Count: {win_count}, Loss Count: {loss_count}, Total Profit: {total_profit}")
    return total_profit


# Streamlit UI for Strategy Application
st.title("Strategy Signal Dashboard")

# User Inputs for Symbol, Market, Interval, Auto Trade
symbol = st.text_input("Enter Symbol (e.g., EURUSD)", "EURUSD")
market = st.selectbox("Select Market", ["forex", "nse"])
interval_map = {"1 Minute": 60, "5 Minutes": 300, "15 Minutes": 900, "1 Hour": 3600}
interval_str = st.selectbox("Select Interval", list(interval_map.keys()))
interval = interval_map[interval_str]

auto_trade = st.checkbox("Enable Auto Trade?")
strategy_type = st.radio("Select Strategy Type", ["Predefined", "Custom"])

# Fetch Tick Data
if st.button("Fetch Latest Tick Data"):
    df = fetch_tick_data(symbol, market, interval)
    if not df.empty:
        st.write(f"Latest Data for {symbol}:")
        st.dataframe(df.tail(10), use_container_width=True)

        # Display Candlestick Chart
        plot_candlestick(df)

        # Apply Strategy and Show Action
        if strategy_type == "Predefined":
            action = apply_strategy(df, "RSI Oversold", interval)
            st.write(f"Action: {action}")
        else:
            st.write("No custom strategy applied yet.")

# Backtesting Button
if st.button("Run Backtesting"):
    if not df.empty:
        total_profit = backtest_strategy(df, "RSI Oversold")
        st.write(f"Total Profit from Backtesting: {total_profit}")
    else:
        st.warning("Please fetch tick data first.")

# Manual Order (optional feature)
if auto_trade and st.button("Execute Auto Trade"):
    st.write("Auto Trade Executed - Placeholder Logic")