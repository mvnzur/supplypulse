import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="SupplyPulse", layout="wide", initial_sidebar_state="expanded")

# Modern Styling with Drop Shadows
st.markdown("""
<style>
    .main {background-color: #f8fafc;}
    .stButton>button {
        border-radius: 12px; 
        height: 48px; 
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .vendor-card {
        background: white;
        border-radius: 16px;
        padding: 20px;
        margin: 12px 0;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        transition: transform 0.2s;
    }
    .vendor-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12);
    }
    .material-circle {
        width: 145px; height: 145px; 
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 16px; font-weight: 700; color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        margin: 15px auto;
        transition: all 0.3s;
    }
    .material-circle:hover {
        transform: scale(1.08);
        box-shadow: 0 15px 40px rgba(0,0,0,0.2);
    }
    h1, h2, h3 {font-family: 'Segoe UI', sans-serif;}
</style>
""", unsafe_allow_html=True)

st.title("🌐 SupplyPulse")
st.markdown("**Modern Procurement Intelligence Platform**")

# Search + Filters
col1, col2 = st.columns([3, 1])
with col1:
    search = st.text_input("🔍 Search Materials or Vendors", placeholder="Lithium, Glencore, Steel...")
with col2:
    category = st.selectbox("Category", ["All", "Battery Materials", "Metals", "Steel"])

# Data
materials = {
    "Lithium": {"ticker": "LIT", "color": "#00BFFF", "price": 28500, "risk": 82, "category": "Battery Materials"},
    "Copper": {"ticker": "CPER", "color": "#FF6B00", "price": 9200, "risk": 65, "category": "Metals"},
    "Steel": {"ticker": "XME", "color": "#4A90E2", "price": 1450, "risk": 58, "category": "Steel"},
    "Nickel": {"ticker": "NUE", "color": "#E74C3C", "price": 18500, "risk": 78, "category": "Metals"}
}

vendors = {
    "Albemarle Corp": {"material": "Lithium", "price": 29200, "lead": "45 days", "reliability": "92%", "risk": "Medium", "loc": "Chile/USA"},
    "Glencore": {"material": "Copper", "price": 9350, "lead": "30 days", "reliability": "88%", "risk": "Low", "loc": "Global"},
    "ArcelorMittal": {"material": "Steel", "price": 1380, "lead": "25 days", "reliability": "95%", "risk": "Low", "loc": "Europe"},
    "Sumitomo": {"material": "Nickel", "price": 19200, "lead": "60 days", "reliability": "85%", "risk": "High", "loc": "Japan"}
}

# Main Content
st.subheader(f"Procurement Dashboard — AutoForge Motors")

# Materials Row
st.markdown("### Raw Materials")
cols = st.columns(4)
for i, (name, info) in enumerate(materials.items()):
    with cols[i]:
        if st.button(name, key=f"mat_{name}", use_container_width=True):
            st.session_state.selected = ("material", name)
        st.markdown(f'<div style="background-color:{info["color"]}" class="material-circle">{name}</div>', unsafe_allow_html=True)
        st.metric(label="", value=f"${info['price']:,}", delta=f"Risk {info['risk']}%")

# Vendors Section
st.markdown("### Approved Vendors")
for name, v in vendors.items():
    with st.container():
        if st.button(f"View {name}", key=f"ven_{name}"):
            st.session_state.selected = ("vendor", name)
        st.markdown(f"""
        <div class="vendor-card">
            <h4>{name}</h4>
            <b>Material:</b> {v['material']} &nbsp;&nbsp; 
            <b>Price:</b> ${v['price']:,} &nbsp;&nbsp;
            <b>Lead Time:</b> {v['lead']} &nbsp;&nbsp;
            <b>Reliability:</b> {v['reliability']}
        </div>
        """, unsafe_allow_html=True)

# Detail View
if "selected" in st.session_state:
    typ, item = st.session_state.selected
    if typ == "vendor":
        v = vendors[item]
        st.title(f"Vendor Profile: {item}")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Contract Price", f"${v['price']:,}")
            st.metric("Lead Time", v['lead'])
        with col2:
            st.metric("Reliability", v['reliability'])
            st.metric("Risk Level", v['risk'])
        st.write(f"**Location:** {v['loc']}")
        
        if st.button("← Back to Dashboard"):
            del st.session_state.selected

st.caption("SupplyPulse • Modern Procurement Intelligence")
