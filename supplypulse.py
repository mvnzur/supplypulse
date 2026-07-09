import streamlit as st
import yfinance as yf
import pandas as pd
import json
import os
from datetime import datetime

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

if "portfolio" not in st.session_state:
    st.session_state.portfolio = load_portfolio()

if "selected_material" not in st.session_state:
    st.session_state.selected_material = None

if "live_vendors" not in st.session_state:
    st.session_state.live_vendors = {}

# ==================== DATA ====================
all_materials = {
    "Lithium": "LIT", "Copper": "CPER", "Crude Oil": "CL=F",
    "Steel": "XME", "Nickel": "NUE", "Gold": "GC=F",
    "Aluminum": "AL=F", "Natural Gas": "NG=F"
}

sae_standards = [
    {"Code": "SAE J403", "Title": "Chemical Compositions of SAE Carbon Steels", "Category": "Materials - Steel"},
    {"Code": "SAE J404", "Title": "Chemical Compositions of SAE Alloy Steels", "Category": "Materials - Steel"},
    {"Code": "SAE AMS 5643", "Title": "Steel, Corrosion-Resistant", "Category": "Materials - Stainless Steel"},
    {"Code": "SAE AMS 4911", "Title": "Titanium Alloy Sheet and Plate", "Category": "Materials - Titanium"},
    {"Code": "SAE AMS 4027", "Title": "Aluminum Alloy Sheet and Plate", "Category": "Materials - Aluminum"},
    {"Code": "SAE J431", "Title": "Automotive Gray Iron Castings", "Category": "Materials - Cast Iron"},
    {"Code": "SAE J434", "Title": "Automotive Ductile Iron Castings", "Category": "Materials - Cast Iron"},
    {"Code": "SAE J3016", "Title": "Levels of Driving Automation", "Category": "Automotive - Autonomy"},
    {"Code": "SAE J1772", "Title": "Electric Vehicle Conductive Charge Coupler", "Category": "Automotive - EV"},
]

def get_live_data(ticker):
    try:
        data = yf.Ticker(ticker).history(period="5d")
        if not data.empty:
            price = round(data['Close'].iloc[-1], 2)
            change = round(data['Close'].pct_change().iloc[-1] * 100, 2)
            return price, change
    except:
        pass
    return None, None

# ==================== LIVE VENDOR SEARCH ====================
def search_live_vendors(item):
    """Simulates live vendor search based on material/standard"""
    item_lower = item.lower()
    
    # Smart mapping for live-style results
    if "steel" in item_lower or "j403" in item_lower or "j404" in item_lower:
        return ["ArcelorMittal", "Nippon Steel", "POSCO", "Tata Steel", "Baosteel"]
    elif "titanium" in item_lower or "ams 4911" in item_lower:
        return ["TIMET", "VSMPO-AVISMA", "Howmet Aerospace", "Allegheny Technologies"]
    elif "aluminum" in item_lower or "ams 4027" in item_lower:
        return ["Alcoa", "Novelis", "Constellium", "Kaiser Aluminum"]
    elif "lithium" in item_lower:
        return ["Albemarle", "SQM", "Ganfeng Lithium", "Tianqi Lithium"]
    elif "copper" in item_lower:
        return ["Glencore", "BHP", "Freeport-McMoRan", "Rio Tinto"]
    elif "nickel" in item_lower:
        return ["Vale", "Norilsk Nickel", "BHP", "Glencore"]
    elif "cast iron" in item_lower or "j431" in item_lower or "j434" in item_lower:
        return ["Waupaca Foundry", "Grede Holdings", "Fonderie de Bretagne"]
    elif "ev" in item_lower or "j1772" in item_lower:
        return ["Tesla", "ChargePoint", "EVgo", "Blink Charging"]
    else:
        return ["Major Global Supplier A", "Major Global Supplier B", "Regional Supplier"]

# ==================== NAVIGATION ====================
st.sidebar.title("🌐 SupplyPulse")
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Commodities", "My Portfolio", "Standards", "Markets"],
    index=0
)

# ==================== PAGE: STANDARDS ====================
if page == "Standards":
    st.title("SAE Standards Search")

    search = st.text_input("Search Standards", placeholder="J403, Steel, Titanium...")

    filtered = [s for s in sae_standards if search.lower() in s["Code"].lower() or search.lower() in s["Title"].lower()]

    if filtered:
        df = pd.DataFrame(filtered)
        st.dataframe(df, use_container_width=True, hide_index=True)

        selected = st.selectbox("Select Standard", [s["Code"] for s in filtered])

        if st.button("Add to Portfolio", type="primary"):
            if selected not in st.session_state.portfolio:
                st.session_state.portfolio.append(selected)
                save_portfolio(st.session_state.portfolio)
                st.success(f"Added {selected}")
                st.rerun()
    else:
        st.info("No standards found.")

# ==================== PAGE: MY PORTFOLIO ====================
elif page == "My Portfolio":
    st.title("My Portfolio")

    with st.expander("＋ Add Item"):
        col1, col2 = st.columns([2, 1])
        with col1:
            choice = st.selectbox("Select Material", list(all_materials.keys()))
        with col2:
            custom = st.text_input("Custom / Standard Name")

        if st.button("Add"):
            name = custom.strip() if custom.strip() else choice
            if name not in st.session_state.portfolio:
                st.session_state.portfolio.append(name)
                save_portfolio(st.session_state.portfolio)
                st.success(f"Added {name}")
                st.rerun()

    st.subheader("Tracked Items")

    for item in st.session_state.portfolio:
        with st.container(border=True):
            cols = st.columns([4, 3, 3])
            with cols[0]:
                st.write(f"**{item}**")
            with cols[1]:
                if item in all_materials:
                    price, change = get_live_data(all_materials[item])
                    st.metric("Price", f"${price}" if price else "N/A")
            with cols[2]:
                if st.button("View", key=f"view_{item}"):
                    st.session_state.selected_material = item
                    st.rerun()
                if st.button("Remove", key=f"remove_{item}"):
                    st.session_state.portfolio.remove(item)
                    save_portfolio(st.session_state.portfolio)
                   