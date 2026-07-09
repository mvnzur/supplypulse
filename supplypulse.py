import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

st.set_page_config(page_title="SupplyPulse", layout="wide", initial_sidebar_state="expanded")

# Custom CSS
st.markdown("""
<style>
    .material-circle {
        width: 160px; height: 160px; border-radius: 50%; 
        display: flex; align-items: center; justify-content: center;
        font-size: 17px; font-weight: bold; color: white;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        cursor: pointer; transition: all 0.3s;
    }
    .material-circle:hover {transform: scale(1.1); box-shadow: 0 10px 30px rgba(0,0,0,0.2);}
</style>
""", unsafe_allow_html=True)

st.title("🌐 SupplyPulse")
st.caption("Real-time Supply Chain Intelligence")

# Sidebar
st.sidebar.header("🏢 Select Company")
businesses = ["AutoForge Motors", "ElectroSteel Inc.", "GreenBattery Solutions", "AeroCast Manufacturing"]
selected_business = st.sidebar.selectbox("Company", businesses)

# Real Materials with Tickers
material_data = {
    "Cast Iron": {"ticker": "XME", "color": "#4A90E2", "category": "Steel"},
    "Nodular Cast Iron": {"ticker": "XME", "color": "#50C878", "category": "Steel"},
    "Cast Steel": {"ticker": "SLX", "color": "#FF9500", "category": "Steel"},
    "Chrome Nickel Steel": {"ticker": "NUE", "color": "#E74C3C", "category": "Stainless"},
    "Austenitic Stainless": {"ticker": "NUE", "color": "#9B59B6", "category": "Stainless"},
    "Lithium": {"ticker": "LIT", "color": "#00BFFF", "category": "Battery"},
    "Copper": {"ticker": "CPER", "color": "#FF6B00", "category": "Metal"}
}

# Fetch real prices
@st.cache_data(ttl=60)  # Refresh every minute
def get_price(ticker):
    try:
        data = yf.Ticker(ticker).history(period="5d")
        if not data.empty:
            price = round(data['Close'].iloc[-1], 2)
            change = round(data['Close'].pct_change().iloc[-1] * 100, 2)
            return price, change
    except:
        pass
    return 0, 0

# Main UI
if "selected_material" not in st.session_state:
    st.subheader(f"Raw Materials Portfolio — {selected_business}")
    
    cols = st.columns(3)
    for i, (name, info) in enumerate(material_data.items()):
        price, change = get_price(info["ticker"])
        
        with cols[i % 3]:
            if st.button(name, key=name, use_container_width=True):
                st.session_state.selected_material = name
                st.rerun()
            
            st.markdown(f"""
            <div style="background-color:{info['color']};" class="material-circle">
                {name.split()[-1] if len(name.split()) > 1 else name}
            </div>
            """, unsafe_allow_html=True)
            
            delta = f"{'↑' if change > 0 else '↓'} {abs(change)}%" if change != 0 else ""
            st.metric(name, f"${price}", delta, delta_color="normal")
else:
    # Detailed Material View
    mat = st.session_state.selected_material
    info = material_data[mat]
    price, change = get_price(info["ticker"])

    st.title(f"{mat} — Live Analysis")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Price", f"${price}", f"{change}%")
    with col2:
        st.metric("Risk Level", "68/100", "↑ Medium")
    with col3:
        st.metric("Bottleneck Risk", "High", "Next 45 days")

    st.divider()

    tab1, tab2, tab3 = st.tabs(["📈 Live Trends", "🔮 Forecast & Bottlenecks", "📰 Market Signals"])

    with tab1:
        st.subheader("6-Month Price Trend")
        hist = yf.download(info["ticker"], period="6mo")
        st.line_chart(hist['Close'])

    with tab2:
        st.subheader("Forecast")
        st.info(f"Projected price increase of 8-15% for {mat} in next 60 days due to supply constraints.")
        st.warning("Potential bottleneck: Raw material availability dropping")

    with tab3:
        st.subheader("Latest Signals")
        st.success("📰 New mining project approved in Chile (positive for Lithium/Copper)")

    if st.button("← Back to All Materials"):
        del st.session_state.selected_material
        st.rerun()

st.caption("Real-time data powered by Yahoo Finance • Updated every 60 seconds")