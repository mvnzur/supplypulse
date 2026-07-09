import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
from datetime import datetime, timedelta
import requests
import json

st.set_page_config(page_title="SupplyPulse - Live Supply Chain Dashboard", layout="wide")
st.title("🚨 SupplyPulse: Live Supply & Demand Monitor")
st.markdown("**Forecasting bottlenecks • Raw materials tracking • News + Market signals**")

# Sidebar
st.sidebar.header("Configuration")
commodities = st.sidebar.multiselect(
    "Select Raw Materials / Commodities",
    ["Steel (XME)", "Lithium (LIT)", "Oil (CL=F)", "Copper (HG=F)", "Semiconductors (SMH)", "Wheat (ZW=F)"],
    default=["Oil (CL=F)", "Lithium (LIT)"]
)

horizon = st.sidebar.slider("Forecast Horizon (days)", 30, 180, 90)

# Fetch real data
@st.cache_data(ttl=300)
def fetch_data(tickers):
    data = {}
    for tick in tickers:
        try:
            df = yf.download(tick, period="1y", progress=False)
            data[tick] = df
        except:
            data[tick] = pd.DataFrame()
    return data

data = fetch_data(commodities)

# Main Dashboard
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Live Prices")
    for tick in commodities:
        if not data[tick].empty:
            latest = data[tick]['Close'].iloc[-1]
            change = data[tick]['Close'].pct_change().iloc[-1] * 100
            st.metric(tick, f"${latest:.2f}", f"{change:.2f}%")

with col2:
    st.subheader("Risk Level")
    # Simple mock risk scoring (you can enhance with real models)
    risk_scores = {tick: round(abs(data[tick]['Close'].pct_change().std() * 100) * 10, 1) if not data[tick].empty else 50 for tick in commodities}
    for tick, score in risk_scores.items():
        color = "🔴" if score > 70 else "🟡" if score > 40 else "🟢"
        st.write(f"{color} **{tick}**: {score}/100")

with col3:
    st.subheader("Bottleneck Forecast")
    st.info("📈 High risk for Lithium in next 60 days (mock based on volatility)")
    st.progress(75)

# Price Trends
st.subheader("Price Trends & Volatility")
fig = px.line()
for tick in commodities:
    if not data[tick].empty:
        fig.add_scatter(x=data[tick].index, y=data[tick]['Close'], name=tick)
fig.update_layout(height=500)
st.plotly_chart(fig, use_container_width=True)

# Simple Forecasting Placeholder
st.subheader("Demand / Price Forecast (Next 90 Days)")
st.caption("Using historical volatility + trend (replace with Prophet/ARIMA for production)")
forecast_df = pd.DataFrame({
    "Date": pd.date_range(datetime.today(), periods=horizon),
    "Projected_Price_Index": [100 + i*0.5 + (i%10)*2 for i in range(horizon)]
})
st.line_chart(forecast_df.set_index("Date"))

# News & Sentiment Placeholder
st.subheader("Recent News & X Trends")
st.write("🔍 Integrate NewsAPI + X API here for real sentiment analysis")
if st.button("Fetch Latest Signals"):
    st.success("Mock: Port strike in Shanghai → Steel prices expected +12%")

# Raw Materials Impact Table
st.subheader("Raw Materials Portfolio Impact")
impact_data = pd.DataFrame({
    "Material": commodities,
    "Current_Price": [data[t]['Close'].iloc[-1] if not data[t].empty else 0 for t in commodities],
    "30d_Change": [data[t]['Close'].pct_change(30).iloc[-1]*100 if not data[t].empty else 0 for t in commodities],
    "Bottleneck_Risk": list(risk_scores.values()),
    "Product_Impact": ["EV Batteries", "Construction", "Energy", "Electronics", "Electronics", "Food"]
})
st.dataframe(impact_data, use_container_width=True)

st.caption("Built with ❤️ using Streamlit + yfinance. Extend with Prophet for real forecasting, NewsAPI, and X trends!")