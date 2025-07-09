import os
os.system("pip install tensorflow==2.15")

# Now import it
import tensorflow as tf

from PIL import Image
import json
from streamlit_lottie import st_lottie

# --- Page config ---
st.set_page_config(page_title="TCS Algo Trading", layout="wide")

# --- Load logo and animation ---
logo = Image.open("assests/Logo.png")

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

lottie_animation = load_lottiefile("assests/thinkingtrader.json")

# --- Initialize session state ---
if "page" not in st.session_state:
    st.session_state.page = st.query_params.get("page", "home")

# Redirect logic after login/signup success
if st.session_state.get("signup_success") or st.session_state.get("login_success"):
    st.session_state.page = "predict"
    st.session_state.signup_success = False
    st.session_state.login_success = False
    st.rerun()

# --- Page Routing ---
if st.session_state.page == "home":
    st.markdown("""<style>
    [data-testid="stAppViewContainer"] {
        background-color: black;
        padding: 0rem 2rem;
    }
    .stButton > button {
        font-size: 24px !important;
        font-weight: bold !important;
        padding: 12px 24px !important;
        color: white !important;
        background-color: #2e2e2e !important;
        border: 1px solid #444 !important;
        border-radius: 12px !important;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #00bfff !important;
        color: black !important;
        transform: scale(1.05);
        box-shadow: 0 0 15px #00bfff;
    }
    .card-container {
        background-color: #1e1e1e;
        border-radius: 15px;
        padding: 20px;
        color: white;
        box-shadow: 0 0 15px rgba(0, 191, 255, 0.2);
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 250px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .card-container:hover {
        transform: scale(1.05);
        box-shadow: 0 0 30px #00bfff;
    }
    .card-title {
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 10px;
        color: #00bfff;
    }
    .card-desc {
        font-size: 20px;
        color: #cccccc;
        margin-bottom: 14px;
    }
    </style>""", unsafe_allow_html=True)

    col_logo, _, col_buttons = st.columns([1, 6, 2])
    with col_logo:
        st.image(logo, width=160)
    with col_buttons:
        btn1, btn2 = st.columns([1, 1], gap="small")
        with btn1:
            st.button("Login", on_click=lambda: st.session_state.update({'page': 'login'}), use_container_width=True)
        with btn2:
            st.button("Sign Up", on_click=lambda: st.session_state.update({'page': 'signup'}), use_container_width=True)

    st_lottie(lottie_animation, speed=1, reverse=False, loop=True, quality="high", height=400)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="card-container"><div class="card-title">🔮 Predict Prices</div>'
                    '<div class="card-desc">Forecast stock movements using<br>deep learning models.</div></div>',
                    unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card-container"><div class="card-title">📊 View Graphs</div>'
                    '<div class="card-desc">Explore trends and live market<br>data with powerful visuals.</div></div>',
                    unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="card-container"><div class="card-title">💡 Buy/Sell Signals</div>'
                    '<div class="card-desc">Get real-time trading signals<br>powered by AI insights.</div></div>',
                    unsafe_allow_html=True)

elif st.session_state.page == "signup":
    from signup import render_signup_form
    render_signup_form()

elif st.session_state.page == "login":
    from LoginPage import render_login_form
    render_login_form()

elif st.session_state.page == "predict":
    from predict_page import run_predict_page
    run_predict_page()
