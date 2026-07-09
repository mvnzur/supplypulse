import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="SupplyPulse", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .vendor-card { border: 1px solid #ddd; border-radius: 16px; padding: 16px; margin: 10px 0; background: white; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    .material-circle { width: 130px; height: 130px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 15px; font-weight: bold; color: white; box-shadow: 0 6px 20px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)

st.title("🌐 SupplyPulse")
st.caption("Procurement Intelligence Platform • Inspired by Coupa")

# Search Bar
search = st.text_input("🔍 Search Materials or Vendors", placeholder="e.g. Lithium, Steel Supplier, Tesla vendor...")

# Sidebar
st.sidebar.header("🏢 Company")
company = st.sidebar.selectbox("Select Company", ["AutoForge Motors", "GreenBattery Solutions", "ElectroSteel Inc."])

# Mock Data
materials = {
    "Lithium": {"ticker": "LIT", "color": "#00BFFF", "avg_price": 28500, "risk": 82},
    "Copper": {"ticker": "CPER", "color": "#FF6B00", "avg_price": 9200, "risk": 65},
    "Steel": {"ticker": "XME", "color": "#4A90E2", "avg_price": 1450, "risk": 58},
    "Nickel": {"ticker": "NUE", "color": "#E74C3C", "avg_price": 18500, "risk": 78}
}

vendors = {
    "Albemarle Corp": {"material": "Lithium", "price": 29200, "lead_time": "45 days", "reliability": "92%", "risk": "Medium", "location": "USA / Chile"},
    "Glencore": {"material": "Copper", "price": 9350, "lead_time": "30 days", "reliability": "88%", "risk": "Low", "location": "Global"},
    "ArcelorMittal": {"material": "Steel", "price": 1380, "lead_time": "25 days", "reliability": "95%", "risk": "Low", "location": "Europe"},
    "Sumitomo Metal": {"material": "Nickel", "price": 19200, "lead_time": "60 days", "reliability": "85%", "risk": "High", "location": "Japan"}
}

# Filter based on search
filtered_materials = {k: v for k, v in materials.items() if search.lower() in k.lower()}
filtered_vendors = {k: v for k, v in vendors.items() if search.lower() in k.lower() or search.lower() in v["material"].lower()}

# Main Content
if search:
    st.subheader(f"Results for '{search}'")
else:
    st.subheader(f"Active Procurement — {company}")

# Materials Section
st.markdown("### Raw Materials")
cols = st.columns(4)
for i, (name, data) in enumerate(filtered_materials.items() or materials.items()):
    with cols[i % 4]:
        price, _ = get_price(data["ticker"]) if 'get_price' in globals() else (data["avg_price"], 0)
        if st.button(name, key=f"mat_{name}"):
            st.session_state.selected = ("material", name)
        st.markdown(f'<div style="background:{data["color"]};" class="material-circle">{name}</div>', unsafe_allow_html=True)
        st.metric("", f"${price:,}", f"Risk: {data['risk']}%")

# Vendors Section
st.markdown("### Approved Vendors")
for name, info in filtered_vendors.items() or vendors.items():
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("View", key=f"ven_{name}"):
                st.session_state.selected = ("vendor", name)
        with col2:
            st.markdown(f"""
            <div class="vendor-card">
                <h4>{name}</h4>
                <b>Material:</b> {info['material']} | 
                <b>Price/ton:</b> ${info['price']:,} | 
                <b>Lead Time:</b> {info['lead_time']} | 
                <b>Reliability:</b> {info['reliability']}
            </div>
            """, unsafe_allow_html=True)

# Detailed View
if "selected" in st.session_state:
    typ, item = st.session_state.selected
    if typ == "vendor":
        info = vendors[item]
        st.title(f"Vendor Profile: {item}")
        st.metric("Current Price", f"${info['price']:,}")
        st.write(f"**Material:** {info['material']}")
        st.write(f"**Lead Time:** {info['lead_time']}")
        st.write(f"**Location:** {info['location']}")
        st.write(f"**Risk Level:** {info['risk']}")
        
        if st.button("Back to Dashboard"):
            del st.session_state.selected

    elif typ == "material":
        # You can expand this later
        st.title(f"Material Deep Dive: {item}")
        st.info("Full analytics page would go here (forecasts, multiple vendors, etc.)")
        if st.button("Back"):
            del st.session_state.selected

st.caption("SupplyPulse — Procurement Intelligence Platform")