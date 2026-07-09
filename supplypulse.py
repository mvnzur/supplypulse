import streamlit as st
import yfinance as yf
import random

st.set_page_config(page_title="SupplyPulse", layout="wide")

# Styling
st.markdown("""
<style>
    .portfolio-container {
        display: flex; overflow-x: auto; padding: 20px 0; gap: 25px;
        scrollbar-width: thin;
    }
    .portfolio-container::-webkit-scrollbar { height: 8px; }
    .portfolio-container::-webkit-scrollbar-thumb { background: #ccc; border-radius: 10px; }

    .material-card {
        min-width: 290px; background: white; border-radius: 22px; 
        padding: 25px; box-shadow: 0 15px 40px rgba(0,0,0,0.12);
        transition: all 0.4s; animation: pulse 2.5s infinite ease-in-out;
        cursor: pointer;
    }
    .material-card:hover {
        transform: translateY(-12px) scale(1.04);
        box-shadow: 0 25px 55px rgba(0,0,0,0.2);
    }
    @keyframes pulse { 0%,100% { box-shadow: 0 15px 40px rgba(0,0,0,0.12); } 50% { box-shadow: 0 22px 50px rgba(0,0,0,0.18); } }
</style>
""", unsafe_allow_html=True)

st.title("🌐 SupplyPulse")
st.caption("Real-time Material Portfolio")

# Initialize
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = ["Lithium", "Copper", "Steel"]
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = "wide"  # wide or compact

all_materials = {
    "Lithium": "LIT", "Copper": "CPER", "Crude Oil": "CL=F",
    "Steel": "XME", "Nickel": "NUE", "Gold": "GC=F",
    "Aluminum": "AL=F", "Natural Gas": "NG=F"
}

def get_price(ticker):
    try:
        data = yf.Ticker(ticker).history(period="3d")
        if not data.empty:
            price = round(data['Close'].iloc[-1], 2)
            change = round(data['Close'].pct_change().iloc[-1] * 100, 2)
            return price, change
    except:
        pass
    return None, None

# ================== HEADER ==================
col1, col2, col3 = st.columns([3, 2, 1])
with col1:
    st.subheader("My Materials Portfolio")
with col2:
    st.session_state.view_mode = st.radio("View Mode", ["Wide", "Compact"], horizontal=True, label_visibility="collapsed")
with col3:
    if st.button("＋ Add Material", type="primary"):
        st.session_state.show_add = True

# ================== PORTFOLIO DISPLAY ==================
if st.session_state.portfolio:
    container = st.container()
    with container:
        st.markdown('<div class="portfolio-container">', unsafe_allow_html=True)
        
        hover_colors = ["#FFD700", "#FF4D4D", "#00FFFF"]
        
        for mat in st.session_state.portfolio:
            ticker = all_materials.get(mat, mat)
            price, change = get_price(ticker)
            accent = random.choice(hover_colors)
            
            if st.button(mat, key=f"view_{mat}", use_container_width=True):
                st.session_state.selected = mat
            
            card_width = "min-width: 290px;" if st.session_state.view_mode == "Wide" else "min-width: 220px;"
            st.markdown(f"""
            <div class="material-card" style="{card_width} border-top-color: {accent};">
                <h3>{mat}</h3>
                <h2>${price if price else '—'}</h2>
                <p style="color:{'green' if change and change > 0 else 'red'}">
                    {change if change else ''}%
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("No materials in portfolio yet. Click '+ Add Material' to start.")

# ================== ADD MATERIAL (Persistent) ==================
if st.session_state.get('show_add'):
    with st.expander("➕ Add New Material", expanded=True):
        choice = st.selectbox("Select Material", options=list(all_materials.keys()))
        custom = st.text_input("Or type a custom material name")
