import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

st.set_page_config(page_title="SupplyPulse", layout="wide")

# Styling
st.markdown("""
<style>
    .big-plus { font-size: 120px; text-align: center; cursor: pointer; }
    .material-card { 
        background: white; border-radius: 20px; padding: 20px; 
        box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin: 15px 0;
        transition: all 0.3s;
    }
    .material-card:hover { transform: translateY(-8px); box-shadow: 0 20px 40px rgba(0,0,0,0.15); }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []

# All available materials (expandable)
all_materials = {
    "Lithium": "LIT", "Copper": "CPER", "Crude Oil": "CL=F", 
    "Steel": "XME", "Nickel": "NUE", "Gold": "GC=F",
    "Aluminum": "AL=F", "Natural Gas": "NG=F", "Silver": "SI=F",
    "Palladium": "PA=F", "Zinc": "ZINC", "Cobalt": "COBALT"
}

def get_price(ticker):
    try:
        data = yf.Ticker(ticker).history(period="2d")
        if not data.empty:
            price = round(data['Close'].iloc[-1], 2)
            change = round((data['Close'].iloc[-1] - data['Close'].iloc[-2]) / data['Close'].iloc[-2] * 100, 2)
            return price, change
    except:
        pass
    return None, None

# ================== HOMEPAGE ==================
if not st.session_state.portfolio:
    st.title("SupplyPulse")
    st.markdown("<h1 style='text-align: center; margin-top: 100px;'>Your Materials Portfolio</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='big-plus'>+</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 22px; color: #666;'>Click the + to add your first material</p>", unsafe_allow_html=True)

    if st.button("＋ Add Material", type="primary", use_container_width=True):
        st.session_state.show_add = True
        st.rerun()

else:
    st.title("My Materials Portfolio")
    search = st.text_input("🔍 Search your materials", "")

    # Display portfolio
    cols = st.columns(3)
    for i, mat in enumerate(st.session_state.portfolio):
        if search and search.lower() not in mat.lower():
            continue
        ticker = all_materials.get(mat, mat)
        price, change = get_price(ticker)
        
        with cols[i % 3]:
            if st.button(mat, key=f"view_{mat}"):
                st.session_state.selected = mat
            st.markdown(f"""
            <div class="material-card">
                <h3>{mat}</h3>
                <h2>${price if price else '—'}</h2>
                <p>{change}% today</p>
            </div>
            """, unsafe_allow_html=True)

# ================== ADD MATERIAL MODAL ==================
if st.session_state.get('show_add'):
    with st.form("add_material"):
        st.subheader("Add New Material")
        selected = st.selectbox("Choose Material", options=list(all_materials.keys()))
        custom = st.text_input("Or type custom material name (advanced)")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Add to Portfolio"):
                name = custom if custom else selected
                if name not in st.session_state.portfolio:
                    st.session_state.portfolio.append(name)
                st.session_state.show_add = False
                st.rerun()
        with col2:
            if st.form_submit_button("Cancel"):
                st.session_state.show_add = False
                st.rerun()

# Detail View
if st.session_state.get('selected'):
    mat = st.session_state.selected
    st.title(f"📊 {mat} Analysis")
    ticker = all_materials.get(mat, mat)
    price, change = get_price(ticker)
    
    st.metric("Current Price", f"${price}" if price else "N/A", f"{change}%")
    
    # Chart
    data = yf.download(ticker, period="1y")
    st.line_chart(data['Close'])
    
    if st.button("← Back to Portfolio"):
        del st.session_state.selected
        st.rerun()

st.caption("SupplyPulse • Real-time data from Yahoo Finance")