import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

st.set_page_config(page_title="SupplyPulse", layout="wide")

# Modern Styling
st.markdown("""
<style>
    .vendor-card {background: white; border-radius: 16px; padding: 20px; margin: 12px 0; 
                  box-shadow: 0 8px 25px rgba(0,0,0,0.08); transition: all 0.3s;}
    .vendor-card:hover {transform: translateY(-5px); box-shadow: 0 15px 35px rgba(0,0,0,0.12);}
    .material-circle {width: 145px; height: 145px; border-radius: 50%; display:flex; 
                      align-items:center; justify-content:center; font-size:16px; font-weight:700; 
                      color:white; box-shadow: 0 10px 30px rgba(0,0,0,0.15); margin:15px auto;}
    .material-circle:hover {transform:scale(1.08);}
</style>
""", unsafe_allow_html=True)

st.title("🌐 SupplyPulse")
st.caption("Free & Open Source Commodity Intelligence")

# Free Commodity Tickers (No API Key Needed)
commodities = {
    "Lithium": {"ticker": "LIT", "color": "#00BFFF"},
    "Copper": {"ticker": "CPER", "color": "#FF6B00"},
    "Steel": {"ticker": "XME", "color": "#4A90E2"},
    "Nickel": {"ticker": "NUE", "color": "#E74C3C"},
    "Oil": {"ticker": "CL=F", "color": "#2E8B57"},
    "Gold": {"ticker": "GC=F", "color": "#FFD700"}
}

@st.cache_data(ttl=300)
def get_price(ticker):
    try:
        data = yf.Ticker(ticker).history(period="5d")
        if not data.empty:
            price = round(data['Close'].iloc[-1], 2)
            change = round(data['Close'].pct_change().iloc[-1] * 100, 2)
            return price, change
    except:
        pass
    return None, None

# UI
search = st.text_input("🔍 Search", placeholder="Lithium, Copper...")

st.subheader("Live Commodity Prices")

cols = st.columns(3)
for i, (name, info) in enumerate(commodities.items()):
    with cols[i % 3]:
        price, change = get_price(info["ticker"])
        if st.button(name, key=name):
            st.session_state.selected = name
        
        st.markdown(f'<div style="background:{info["color"]}" class="material-circle">{name}</div>', unsafe_allow_html=True)
        
        if price:
            st.metric(name, f"${price}", f"{change}%")
        else:
            st.write("Data unavailable")

# Vendors Section
st.subheader("Recommended Suppliers")
vendors = {
    "Albemarle": "Lithium leader - Chile/USA",
    "Glencore": "Copper & Nickel - Global",
    "BHP": "Nickel & Copper",
    "ArcelorMittal": "Steel - Europe"
}

for name, desc in vendors.items():
    st.markdown(f"""
    <div class="vendor-card">
        <h4>{name}</h4>
        <p>{desc}</p>
    </div>
    """, unsafe_allow_html=True)

if "selected" in st.session_state:
    name = st.session_state.selected
    st.title(f"Detailed Analysis: {name}")
    price, change = get_price(commodities[name]["ticker"])
    st.metric("Current Price", f"${price}" if price else "N/A")
    st.line_chart(yf.download(commodities[name]["ticker"], period="6mo")['Close'])
    
    if st.button("Back"):
        del st.session_state.selected

st.caption("Data Source: Yahoo Finance (Free & Open) • No API Key Required")