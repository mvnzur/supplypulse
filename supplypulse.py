import streamlit as st
import yfinance as yf
import pandas as pd
import json
import os
from datetime import datetime

st.set_page_config(page_title="SupplyPulse", layout="wide", page_icon="🌐")

# Load portfolio
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

# SAE Standards (you can expand this list)
sae_standards = [
    {"Code": "SAE J403", "Title": "Chemical Compositions of SAE Carbon Steels", "Category": "Materials - Steel"},
    {"Code": "SAE J404", "Title": "Chemical Compositions of SAE Alloy Steels", "Category": "Materials - Steel"},
    {"Code": "SAE AMS 2759", "Title": "Heat Treatment of Steel Parts", "Category": "Materials - Heat Treatment"},
    {"Code": "SAE AMS 5643", "Title": "Steel, Corrosion-Resistant", "Category": "Materials - Stainless Steel"},
    {"Code": "SAE AMS 4911", "Title": "Titanium Alloy Sheet and Plate", "Category": "Materials - Titanium"},
    {"Code": "SAE AMS 4027", "Title": "Aluminum Alloy Sheet and Plate", "Category": "Materials - Aluminum"},
    {"Code": "SAE J431", "Title": "Automotive Gray Iron Castings", "Category": "Materials - Cast Iron"},
    {"Code": "SAE J434", "Title": "Automotive Ductile Iron Castings", "Category": "Materials - Cast Iron"},
    {"Code": "SAE J3016", "Title": "Levels of Driving Automation", "Category": "Automotive - Autonomy"},
    {"Code": "SAE J1772", "Title": "Electric Vehicle Conductive Charge Coupler", "Category": "Automotive - EV"},
    {"Code": "SAE J1939", "Title": "Vehicle Network Standard", "Category": "Automotive - Networking"},
    {"Code": "SAE AS9100", "Title": "Quality Management Systems - Aviation", "Category": "Aerospace - Quality"},
]

all_materials = {"Lithium": "LIT", "Copper": "CPER", "Steel": "XME", "Nickel": "NUE", "Oil": "CL=F"}

def get_price(ticker):
    try:
        data = yf.Ticker(ticker).history(period="5d")
        if not data.empty:
            return round(data['Close'].iloc[-1], 2), round(data['Close'].pct_change().iloc[-1]*100, 2)
    except:
        pass
    return None, None

# Navigation
st.sidebar.title("SupplyPulse")
page = st.sidebar.radio("Pages", ["Dashboard", "Commodities", "My Portfolio", "Standards", "Markets"])

if page == "Standards":
    st.title("SAE Standards Search")
    search = st.text_input("Search by code or title")

    filtered = [s for s in sae_standards if search.lower() in s["Code"].lower() or search.lower() in s["Title"].lower()]

    if filtered:
        df = pd.DataFrame(filtered)
        st.dataframe(df, use_container_width=True)

        selected = st.selectbox("Select to add to portfolio", [s["Code"] for s in filtered])
        if st.button("Add to Portfolio"):
            if selected not in st.session_state.portfolio:
                st.session_state.portfolio.append(selected)
                save_portfolio(st.session_state.portfolio)
                st.success(f"Added {selected}")
    else:
        st.info("No results. Try broadening your search.")

elif page == "My Portfolio":
    st.title("My Portfolio")
    # ... (your existing portfolio code can go here)

elif page == "Commodities":
    st.title("Commodities")
    for name, ticker in all_materials.items():
        price, change = get_price(ticker)
        st.write(f"**{name}**: ${price} ({change}%)")

# Add other pages as needed...