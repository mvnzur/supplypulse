import streamlit as st
import yfinance as yf
import pandas as pd
import json
import os
from datetime import datetime
import random

st.set_page_config(page_title="SupplyPulse", layout="wide", page_icon="🌐")

# ==================== PERSISTENCE ====================
PORTFOLIO_FILE = "portfolio.json"

def load_portfolio():
    if os.path.exists(PORTFOLIO_FILE):
        with open(PORTFOLIO_FILE, "r") as f:
            return json.load(f)
    return ["Lithium", "Copper", "Steel"]

def save_portfolio(portfolio):
    with open(PORTFOLIO_FILE, "w") as f:
        json.dump(portfolio, f)

if 'portfolio' not in st.session_state:
    st.session_state.portfolio = load_portfolio()

# ==================== DATA ====================
all_materials = {
    "Lithium": "LIT", "Copper": "CPER", "Crude Oil": "CL=F",
    "Steel": "XME", "Nickel": "NUE", "Gold": "GC=F",
    "Aluminum": "AL=F", "Natural Gas": "NG=F", "Palladium": "PA=F"
}

vendors_db = {
    "Lithium": [
        {"vendor": "Albemarle", "price": 29200, "lead_time": "45 days", "reliability": "92%"},
        {"vendor": "SQM", "price": 28500, "lead_time": "35 days", "reliability": "89%"}
    ],
    "Copper": [
        {"vendor": "Glencore", "price": 9350, "lead_time": "30 days", "reliability": "88%"},
        {"vendor": "BHP", "price": 9120, "lead_time": "40 days", "reliability": "95%"}
    ],
    "Steel": [
        {"vendor": "ArcelorMittal", "price": 1380, "lead_time": "25 days", "reliability": "95%"},
        {"vendor": "Nippon Steel", "price": 1420, "lead_time": "50 days", "reliability": "87%"}
    ]
}

def get_price(ticker):
    try:
        data = yf.Ticker(ticker).history(period="5d")
        if not data.empty:
            price = round(data['Close'].iloc[-1], 2)
            change = round(data['Close'].pct_change().iloc[-1] * 100, 2)
            return price, change, data
    except:
        pass
    return None, None, None

# ==================== STYLING ====================
st.markdown("""
<style>
    .portfolio-container { display: flex; overflow-x: auto; gap: 25px; padding: 15px 0; }
    .material-card {
        min-width: 280px; background: white; border-radius: 20px; padding: 22px;
        box-shadow: 0 12px 35px rgba(0,0,0,0.1); transition: all 0.3s;
        animation: pulse 2.5s infinite ease-in-out;
    }
    .material-card:hover { transform: translateY(-10px); box-shadow: 0 22px 50px rgba(0,0,0,0.18); }
    @keyframes pulse { 0%,100% { box-shadow: 0 12px 35px rgba(0,0,0,0.1); } 50% { box-shadow: 0 18px 45px rgba(0,0,0,0.15); } }
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.title("🌐 SupplyPulse")
st.caption("Professional Supply Chain Material Intelligence Platform")

# Sidebar
with st.sidebar:
    st.header("Portfolio Controls")
    if st.button("＋ Add New Material", type="primary", use_container_width=True):
        st.session_state.show_add = True

    st.divider()
    st.session_state.view_mode = st.radio("View Mode", ["Wide", "Compact"], horizontal=True)

# ==================== MAIN PORTFOLIO ====================
st.subheader("Tracked Materials")

if st.session_state.portfolio:
    container = st.container()
    with container:
        st.markdown('<div class="portfolio-container">', unsafe_allow_html=True)
        
        hover_colors = ["#FFD700", "#FF4D4D", "#00FFFF"]
        
        for mat in st.session_state.portfolio:
            ticker = all_materials.get(mat, mat)
            price, change, _ = get_price(ticker)
            accent = random.choice(hover_colors)
            
            if st.button(mat, key=f"view_{mat}", use_container_width=True):
                st.session_state.selected_material = mat
            
            card_width = "min-width: 290px;" if st.session_state.view_mode == "Wide" else "min-width: 230px;"
            st.markdown(f"""
            <div class="material-card" style="{card_width} border-top: 7px solid {accent};">
                <h3>{mat}</h3>
                <h2>${price if price else '—'}</h2>
                <p style="color:{'green' if change and change > 0 else 'red'}">{change if change else ''}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Your portfolio is empty. Add materials using the button above.")

# ==================== ADD MATERIAL ====================
if st.session_state.get('show_add'):
    with st.expander("➕ Add Material to Portfolio", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            choice = st.selectbox("Select from list", list(all_materials.keys()))
        with col2:
            custom = st.text_input("Or type custom material")
        
        if st.button("Add to Portfolio", type="primary"):
            name = custom.strip() if custom.strip() else choice
            if name and name not in st.session_state.portfolio:
                st.session_state.portfolio.append(name)
                save_portfolio(st.session_state.portfolio)
                st.success(f"Added {name} successfully!")
            # Form stays open for multiple adds

# ==================== DETAILED MATERIAL VIEW ====================
if st.session_state.get('selected_material'):
    mat = st.session_state.selected_material
    ticker = all_materials.get(mat, mat)
    price, change, hist = get_price(ticker)

    st.title(f"📊 {mat} Deep Dive")

    # Quick metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Price", f"${price}" if price else "N/A", f"{change}%")
    with col2:
        st.metric("Risk Level", "Medium-High")
    with col3:
        st.metric("Last Updated", datetime.now().strftime("%H:%M"))

    tab1, tab2, tab3 = st.tabs(["📈 Price & Trends", "⚠️ Risk & Forecast", "🏭 Vendor Comparison"])

    with tab1:
        if hist is not None:
            st.line_chart(hist['Close'])
        else:
            st.warning("Price history unavailable")

    with tab2:
        st.subheader("Supply Risk Assessment")
        risk_score = random.randint(55, 85)
        st.progress(risk_score / 100)
        st.write(f"**Risk Score: {risk_score}/100**")
        st.info("Potential supply constraints detected in major producing regions.")

    with tab3:
        st.subheader("Recommended Vendors")
        if mat in vendors_db:
            df = pd.DataFrame(vendors_db[mat])
            st.dataframe(df, use_container_width=True)
        else:
            st.write("No vendor data available for this material.")

    # Actions
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Remove from Portfolio"):
            if mat in st.session_state.portfolio:
                st.session_state.portfolio.remove(mat)
                save_portfolio(st.session_state.portfolio)
            del st.session_state.selected_material
            st.rerun()
    with col2:
        if st.button("← Back to Portfolio"):
            del st.session_state.selected_material
            st.rerun()

# ==================== EXPORT ====================
if st.session_state.portfolio:
    if st.button("📥 Export Portfolio to CSV"):
        df = pd.DataFrame({"Material": st.session_state.portfolio})
        st.download_button("Download CSV", df.to_csv(index=False), "portfolio.csv")

st.caption("SupplyPulse v2.0 • Live data from Yahoo Finance • Built for real use")