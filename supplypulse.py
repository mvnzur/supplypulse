import streamlit as st
import yfinance as yf
import pandas as pd
import json
import os
from datetime import datetime
import random

st.set_page_config(
    page_title="SupplyPulse",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CONFIG & PERSISTENCE ====================
PORTFOLIO_FILE = "portfolio.json"

def load_portfolio():
    if os.path.exists(PORTFOLIO_FILE):
        with open(PORTFOLIO_FILE, "r") as f:
            return json.load(f)
    return ["Lithium", "Copper", "Steel"]

def save_portfolio(portfolio):
    with open(PORTFOLIO_FILE, "w") as f:
        json.dump(portfolio, f)

if "portfolio" not in st.session_state:
    st.session_state.portfolio = load_portfolio()

if "selected_material" not in st.session_state:
    st.session_state.selected_material = None

# ==================== DATA ====================
all_materials = {
    "Lithium": "LIT",
    "Copper": "CPER",
    "Crude Oil": "CL=F",
    "Steel": "XME",
    "Nickel": "NUE",
    "Gold": "GC=F",
    "Aluminum": "AL=F",
    "Natural Gas": "NG=F",
    "Palladium": "PA=F"
}

vendors_data = {
    "Lithium": [
        {"Vendor": "Albemarle", "Price": 29200, "Lead Time": "45 days", "Reliability": "92%"},
        {"Vendor": "SQM", "Price": 28500, "Lead Time": "35 days", "Reliability": "89%"}
    ],
    "Copper": [
        {"Vendor": "Glencore", "Price": 9350, "Lead Time": "30 days", "Reliability": "88%"},
        {"Vendor": "BHP", "Price": 9120, "Lead Time": "40 days", "Reliability": "95%"}
    ],
    "Steel": [
        {"Vendor": "ArcelorMittal", "Price": 1380, "Lead Time": "25 days", "Reliability": "95%"},
        {"Vendor": "Nippon Steel", "Price": 1420, "Lead Time": "50 days", "Reliability": "87%"}
    ]
}

def get_live_data(ticker):
    try:
        ticker_obj = yf.Ticker(ticker)
        hist = ticker_obj.history(period="5d")
        if not hist.empty:
            price = round(hist["Close"].iloc[-1], 2)
            change = round(hist["Close"].pct_change().iloc[-1] * 100, 2)
            return price, change, hist
    except Exception:
        pass
    return None, None, None

# ==================== STYLING ====================
st.markdown("""
<style>
    .main-header {font-size: 2.2rem; font-weight: 700; margin-bottom: 0.5rem;}
    .section-header {font-size: 1.5rem; font-weight: 600; margin-top: 1rem;}
    .metric-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        margin-bottom: 1rem;
    }
    .stButton>button {border-radius: 8px;}
</style>
""", unsafe_allow_html=True)

# ==================== SIDEBAR NAVIGATION ====================
st.sidebar.title("🌐 SupplyPulse")
st.sidebar.caption("Professional Supply Chain Intelligence")

page = st.sidebar.radio(
    "Navigate",
    ["Dashboard", "Commodities", "My Portfolio", "Markets", "Risk & Alerts"],
    index=0
)

st.sidebar.divider()

if st.sidebar.button("Refresh All Data"):
    st.rerun()

st.sidebar.caption("Data source: Yahoo Finance")

# ==================== PAGE: DASHBOARD ====================
if page == "Dashboard":
    st.markdown('<p class="main-header">Dashboard</p>', unsafe_allow_html=True)
    st.caption(f"Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Tracked Materials", len(st.session_state.portfolio))
    with col2:
        st.metric("High Risk Items", "2")
    with col3:
        st.metric("Avg Price Change", "+2.8%")
    with col4:
        st.metric("Portfolio Health", "Stable")

    st.divider()

    st.subheader("Quick Portfolio Overview")
    if st.session_state.portfolio:
        quick_data = []
        for mat in st.session_state.portfolio:
            ticker = all_materials.get(mat, mat)
            price, change, _ = get_live_data(ticker)
            quick_data.append({
                "Material": mat,
                "Price": price,
                "Change %": change
            })
        st.dataframe(pd.DataFrame(quick_data), use_container_width=True, hide_index=True)
    else:
        st.info("Add materials in the My Portfolio section to see overview.")

# ==================== PAGE: COMMODITIES ====================
elif page == "Commodities":
    st.markdown('<p class="main-header">Commodities</p>', unsafe_allow_html=True)
    st.caption("Live prices for key industrial and energy commodities")

    search_term = st.text_input("Search Materials", placeholder="Type to filter...")

    filtered_materials = {k: v for k, v in all_materials.items() 
                          if search_term.lower() in k.lower()}

    table_data = []
    for name, ticker in filtered_materials.items():
        price, change, _ = get_live_data(ticker)
        table_data.append({
            "Material": name,
            "Ticker": ticker,
            "Price (USD)": price,
            "Daily Change %": change
        })

    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

    if st.button("Export Commodities to CSV"):
        df.to_csv("commodities_export.csv", index=False)
        st.success("Exported as commodities_export.csv")

# ==================== PAGE: MY PORTFOLIO ====================
elif page == "My Portfolio":
    st.markdown('<p class="main-header">My Portfolio</p>', unsafe_allow_html=True)

    # Add Material Section
    with st.expander("＋ Add New Material to Portfolio", expanded=False):
        col1, col2 = st.columns([2, 1])
        with col1:
            selected = st.selectbox("Select from list", list(all_materials.keys()))
        with col2:
            custom_name = st.text_input("Custom material name (optional)")

        if st.button("Add to Portfolio", type="primary"):
            final_name = custom_name.strip() if custom_name.strip() else selected
            if final_name not in st.session_state.portfolio:
                st.session_state.portfolio.append(final_name)
                save_portfolio(st.session_state.portfolio)
                st.success(f"Successfully added {final_name}")
            else:
                st.warning("Material already exists in portfolio")

    st.subheader("Your Tracked Materials")

    if not st.session_state.portfolio:
        st.info("Your portfolio is currently empty.")
    else:
        for material in st.session_state.portfolio:
            ticker = all_materials.get(material, material)
            price, change, hist = get_live_data(ticker)

            with st.container(border=True):
                cols = st.columns([3, 2, 2, 3])
                with cols[0]:
                    st.write(f"**{material}**")
                with cols[1]:
                    st.metric("Price", f"${price}" if price else "N/A")
                with cols[2]:
                    st.metric("Change", f"{change}%" if change else "N/A")
                with cols[3]:
                    if st.button("View Details", key=f"detail_{material}"):
                        st.session_state.selected_material = material
                    if st.button("Remove", key=f"remove_{material}"):
                        st.session_state.portfolio.remove(material)
                        save_portfolio(st.session_state.portfolio)
                        st.rerun()

    # Detailed View
    if st.session_state.selected_material:
        mat = st.session_state.selected_material
        ticker = all_materials.get(mat, mat)
        price, change, hist = get_live_data(ticker)

        st.divider()
        st.subheader(f"Detailed Analysis: {mat}")

        tab1, tab2, tab3 = st.tabs(["Price History", "Risk Assessment", "Vendors"])

        with tab1:
            if hist is not None:
                st.line_chart(hist["Close"])
            else:
                st.warning("Price history could not be loaded.")

        with tab2:
            st.write("**Supply Risk Score**")
            risk = random.randint(45, 85)
            st.progress(risk / 100)
            st.write(f"Current Risk Level: **{risk}/100**")

        with tab3:
            if mat in vendors_data:
                st.dataframe(pd.DataFrame(vendors_data[mat]), use_container_width=True)
            else:
                st.write("No vendor data available for this material.")

        if st.button("Close Detail View"):
            st.session_state.selected_material = None
            st.rerun()

# ==================== PAGE: MARKETS ====================
elif page == "Markets":
    st.markdown('<p class="main-header">Related Markets</p>', unsafe_allow_html=True)
    st.caption("ETFs and stocks linked to key raw materials")

    market_data = pd.DataFrame({
        "Name": ["Global X Lithium & Battery Tech", "Copper Miners ETF", "Steel ETF", "VanEck Gold Miners"],
        "Ticker": ["LIT", "COPX", "SLX", "GDX"],
        "Last Price": [42.35, 38.90, 65.40, 38.75],
        "Change %": [1.8, -0.9, 2.1, 0.4]
    })
    st.dataframe(market_data, use_container_width=True, hide_index=True)

# ==================== PAGE: RISK & ALERTS ====================
elif page == "Risk & Alerts":
    st.markdown('<p class="main-header">Risk & Alerts</p>', unsafe_allow_html=True)
    st.warning("This is a demo risk module")

    st.subheader("Portfolio Risk Summary")
    st.progress(0.68)
    st.write("**Overall Risk Score: 68/100 (Medium-High)**")

    st.subheader("Active Alerts")
    st.info("Potential supply disruption risk detected for Lithium (next 30-60 days)")
    st.warning("Nickel price volatility increased significantly in the last 7 days")

st.caption("SupplyPulse • Professional Supply Chain Intelligence Platform • v2.1")